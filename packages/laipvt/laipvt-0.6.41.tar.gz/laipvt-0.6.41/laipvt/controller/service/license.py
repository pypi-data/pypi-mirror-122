from __future__ import absolute_import
from __future__ import unicode_literals
import os
import json
from laipvt.interface.serviceinterface import ServiceInterface
from laipvt.handler.middlewarehandler import EtcdConfigHandler
from laipvt.sysutil.util import path_join, log, status_me
from laipvt.controller.middleware.etcd import EtcdController
from laipvt.sysutil.command import GET_POD_INFO, RESTART_DEPLOYMENT, RESTART_DEPLOYMENT_ALL, HELM_LIST, HELM_INSTALL,\
    HELM_INSTALL_TMP



class LicenseController(ServiceInterface):
    def __init__(self, check_result, service_path):
        super(LicenseController, self).__init__(check_result, service_path)
        self.namespaces = ["mid", ]
        self.istio_injection_namespaces = ["mid", ]
        self.project = "mid"

    def _prepare_license_data_file(self, is_renew=False, **kwargs):
        if is_renew:
            lcs_file_path = kwargs.get("license_file")
        else:
            lcs_file_path = path_join(self.service_path.data, "license.lcs")

        log.info("找到lcs授权文件: {}".format(lcs_file_path))
        for server in self.nodes:
            data_path = path_join(self.deploy_dir, "license-manager/data")
            self._exec_command_to_host(cmd="mkdir -p {}".format(data_path), server=server)
            self._send_file(src=lcs_file_path, dest=path_join(data_path, "license.lcs"))

    def _get_etcd_sign(self):
        try:
            with open(self.service_path.etcd_sign, 'r') as fp:
                load_dict = json.load(fp)
                # print(load_dict["publicKey"])
                return load_dict["signature"], load_dict["publicKey"]
        except Exception as e:
            log.error(e)
            exit(2)

    def start_service(self, project, version):
        signature, publicKey = self._get_etcd_sign()

        self._send_file(src=self.service_path.charts, dest=self.service_charts_remote)
        for service, processes in self.service_path.config.services.items():
            for process in processes:
                log.info("{}开始部署".format(process))

                check_cmd = HELM_LIST.format(process, process)
                check_results = self._exec_command_to_host(cmd=check_cmd, server=self.master_host, check_res=False)
                if check_results["code"] == 0:
                    log.warning("{} helm部署记录中已经存在，不做更新，如需要更新，可以先行删除".format(process))

                else:
                    self._create_logs_dir(service)
                    file_path = os.path.join(self.service_charts_remote, process)
                    # print(file_path)
                    cmd = HELM_INSTALL.format(
                        process=process, replicas=self.replicas,
                        registry_hub=path_join(self.registry_hub, project),
                        image_name=process, image_tag=version,
                        pvt_work_dir=self.deploy_dir,
                        etcd_endpoint=self.etcd_endpoint,
                        lm_etcd_sig=signature,
                        lm_etcd_pubkey=publicKey,
                        file_path=file_path)

                    self._exec_command_to_host(cmd=cmd, server=self.master_host)

    def restart_service(self):
        etcd = EtcdController(self.check_result, EtcdConfigHandler(), "")
        etcd.reset()
        get_pod_info_cmd = GET_POD_INFO.format("license-manager")
        res = self._exec_command_to_host(cmd=get_pod_info_cmd, server=self.harbor_hosts[0], check_res=True)
        if not (res["code"] == 0 and "Running" in res["stdout"]):
            log.error("license服务未获取到，请检查:{}".format(get_pod_info_cmd))
            exit(2)
        restart_deployment_cmd =  RESTART_DEPLOYMENT.format("mid", "license-manager")
        self._exec_command_to_host(cmd=restart_deployment_cmd, server=self.harbor_hosts[0], check_res=True)

        restart_all_deployment_cmd = [
            RESTART_DEPLOYMENT_ALL.format("mage"),
            RESTART_DEPLOYMENT_ALL.format("rpa")
        ]
        self._exec_command_to_host(cmd=restart_all_deployment_cmd, server=self.harbor_hosts[0], check_res=True)

    @status_me("middleware")
    def deploy_license(self):
        self._create_namespace(
            namespaces=self.namespaces,
            istio_injection_namespaces=self.istio_injection_namespaces
        )
        self.push_images(project=self.project)
        self._prepare_license_data_file()
        self.start_service(project=self.project, version=self.private_deploy_version)

    def renew_license(self, license_file):
        self._prepare_license_data_file(is_renew=True, license_file=license_file)
        self.restart_service()

    def deploy(self):
        self.deploy_license()
