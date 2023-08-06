from __future__ import absolute_import
from __future__ import unicode_literals

import os
from laipvt.sysutil.ssh import SSHConnect
from laipvt.helper.exception import UtilsError
from laipvt.interface.serviceinterface import ServiceInterface
from laipvt.sysutil.template import FileTemplate
from laipvt.sysutil.util import path_join, log, status_me
from laipvt.sysutil.command import GET_PVC_VOLUMENAME_CMD, RESTART_DEPLOYMENT

def ssh_obj(ip, user, password, port=22) -> SSHConnect:
    return SSHConnect(hostip=ip, username=user, password=password, port=port)


class ChatbotController(ServiceInterface):
    def __init__(self, check_result, service_path):
        super(ChatbotController, self).__init__(check_result, service_path)
        self.namespaces = ["chatbot", "proxy", ]
        self.istio_injection_namespaces = ["chatbot", "mid", ]
        self.project = "chatbot"

        self.templates_src = path_join(self.templates_dir, "env_pvt_templates")
        self.common_dest = path_join("/tmp", "env_pvt_common")
        self.common_remote = path_join(self.deploy_dir, "env_pvt_common")

        self.fill_bin_src = path_join(self.templates_dir, "pvt_gen-linux-amd64")
        self.fill_bin_remote = path_join(self.deploy_dir, "pvt_gen-linux-amd64")

        self.chatbot_config_templates = path_join(self.templates_dir, "chatbot_conf_templates/Chatbot")
        self.chatbot_config_remote = path_join(self.deploy_dir, "chatbot_conf_templates/Chatbot")
        self.chatbot_config_target = path_join(self.deploy_dir, "chatbot_configmap")
        self.chatbot_configmap = path_join(self.chatbot_config_target, "Chatbot")
        self.chatbot_configmap_remote = path_join(self.deploy_dir, "Chatbot")
        self.chatbot_config = path_join(self.deploy_dir, "chatbot_config")
        self.chatbot_app_config_hosts = path_join(self.chatbot_config, "Chatbot/laiye-chatbot-app.conf")
        self.chatbot_app_config_container = "/home/works/program/conf/online.conf"

        self.nginx_template = path_join(self.templates_dir, "nginx/http/nginx-chatbot.tmpl")
        self.nginx_tmp = path_join("/tmp", "nginx-chatbot.conf")
        self.nginx_file_remote = path_join(self.deploy_dir, "nginx/http/nginx-chatbot.conf")

    def _fill_item_file(self):
        log.info("渲染填充项文件{}到{}".format(self.templates_src, self.common_dest))
        try:
            FileTemplate(self.middleware_cfg, self.templates_src, self.common_dest).fill()
        except UtilsError as e:
            log.error(e.msg)
            exit(e.code)
        return True if os.path.isdir(self.common_dest) else False

    def _send_file(self, src, dest, role=""):
        server = self.master_host
        log.info("分发{}到{}:{}".format(src, server.ipaddress, dest))
        ssh_cli = ssh_obj(ip=server.ipaddress, user=server.username, password=server.password, port=server.port)
        try:
            ssh_cli.put(src, dest)
        except Exception as e:
            log.error(e)
            exit(2)
        finally:
            ssh_cli.close()

    def _generic_configmap(self):
        if self._fill_item_file():
            self._send_file(src=self.fill_bin_src, dest=self.fill_bin_remote)
            self._send_file(src=self.common_dest, dest=self.common_remote)
            self._send_file(src=self.chatbot_config_templates, dest=self.chatbot_config_remote)

            cmd = [
                "chmod +x {}".format(self.fill_bin_remote),
                "{} -tmplPath={} -valuePath={} -targetPath={} -configTargetPath={}".format(
                    self.fill_bin_remote,
                    self.chatbot_config_remote,
                    self.common_remote,
                    self.chatbot_config_target,
                    self.chatbot_config
                )
            ]
            log.info(cmd)
            self._exec_command_to_host(cmd=cmd, server=self.servers[0])

    @status_me("chatbot")
    def deploy_chatbot_configmap(self):
        self._generic_configmap()
        self._create_namespace(namespaces=self.namespaces,
                               istio_injection_namespaces=self.istio_injection_namespaces)
        self._send_file(src=self.chatbot_configmap, dest=self.chatbot_configmap_remote)
        cmd = "kubectl apply -f {}".format(self.chatbot_configmap_remote)
        self._exec_command_to_host(cmd=cmd, server=self.harbor_hosts[0])
        self.deploy_istio()

    @status_me("chatbot")
    def init_chatbot_mysql(self):
        log.info("初始化mysql数据")
        # version = self.private_deploy_version.split("-")[0]
        mysql_real_ip = self.master_host.ipaddress
        if not self.middleware_cfg.mysql.is_deploy:
            mysql_real_ip = self.middleware_cfg.mysql.ipaddress[0]

        # docker run -t {进程：chatbot-app} --init
        cmd = "docker run --add-host mysql.default.svc:{} -t -v {}:{} {}/{}/chatbot-app:{} --init".format(
            mysql_real_ip,
            self.chatbot_app_config_hosts, self.chatbot_app_config_container,
            self.registry_hub, self.project, self.private_deploy_version
        )
        res = self._exec_command_to_host(cmd=cmd, server=self.servers[0], check_res=True)
        if res["code"] != 0:
            log.error("初始化mysql数据失败")
            log.error(res["stdout"])
            exit(2)
        log.info("初始化mysql数据完成")

    @status_me("chatbot")
    def push_chatbot_images(self):
        self.push_images(self.project)

    @status_me("chatbot")
    def start_chatbot_service(self):
        self.start_service(project=self.project, version=self.private_deploy_version)

    @status_me("chatbot")
    def chatbot_proxy_on_nginx(self):
        self.proxy_on_nginx(self.nginx_template, self.nginx_tmp, self.nginx_file_remote)

    @status_me("chatbot")
    def prepare_data_chatbot(self):
        for data in self.service_path.config.mount_data:
            # 获取pvc的volumeName
            namespace = self.project
            pvc_name = "{}-{}-{}-claim".format(data["process_name"], data["service_name"], data["relative_path"])
            cmd = GET_PVC_VOLUMENAME_CMD.format(namespace, pvc_name)
            res = self._exec_command_to_host(cmd=cmd, server=self.master_host, check_res=True)
            if res["code"] != 0:
                log.error("获取pvc信息失败")
                log.error(res["stdout"])
                exit(2)
            pvc_volume_name = res["stdout"].strip()
            if not pvc_volume_name:
                log.error("pvc创建失败")
                log.error(res["stdout"])
                exit(2)

            self.chatbot_data_src = path_join(
                self.service_path.data, data["data_name"]
            )
            if self.check_result.use_external_disk:
                # rook-ceph远程位置
                self.chatbot_data_remote = path_join(
                    "/var/lib/kubelet/plugins/kubernetes.io/csi/pv", pvc_volume_name, "globalmount", data["data_name"]
                )
            else:
                # 获取local-path pvc的volumeName
                namespace = "rook-nfs"
                local_pvc_name = "nfs-default-claim"
                cmd = GET_PVC_VOLUMENAME_CMD.format(namespace, local_pvc_name)
                res = self._exec_command_to_host(cmd=cmd, server=self.master_host, check_res=True)
                if res["code"] != 0:
                    log.error("获取local path pvc的volumeName失败")
                    exit(2)
                local_pvc_volume_name = res["stdout"].strip()
                if not local_pvc_volume_name:
                    log.error("获取local path pvc失败")
                    log.error(res["stdout"])
                    exit(2)

                # rook-nfs远程位置
                self.chatbot_data_remote = path_join(
                    self.deploy_dir, "nfs",
                    "{}_{}_{}".format(local_pvc_volume_name, namespace, local_pvc_name),
                    "{}-{}".format(pvc_name, pvc_volume_name)
                )

            self._send_file(src=self.chatbot_data_src, dest=self.chatbot_data_remote)
            namespace = self.project
            restart_deployment_cmd = RESTART_DEPLOYMENT.format(namespace, data["service_name"])
            self._exec_command_to_host(cmd=restart_deployment_cmd, server=self.master_host, check_res=True)

    def run(self):
        self.push_chatbot_images()
        self.deploy_chatbot_configmap()
        self.init_chatbot_mysql()
        self.start_chatbot_service()
        self.chatbot_proxy_on_nginx()
        self.prepare_data_chatbot()
