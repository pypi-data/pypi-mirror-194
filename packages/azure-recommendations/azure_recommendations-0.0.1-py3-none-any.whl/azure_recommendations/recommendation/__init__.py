from azure.identity import ClientSecretCredential
from azure_recommendations.recommendation.utils import utils
from azure_recommendations.recommendation.vm_recommendations import vm_recommendations

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class recommendation(utils, vm_recommendations):
    def __init__(self, tenant_id: str, client_id: str, client_secret: str):
        """
        :param tenant_id: tenant Id from Azure
        :param client_id: Access ID
        :param client_secret: Secret Access ID
        """

        self.credentials = ClientSecretCredential(
            client_id=client_id,
            client_secret=client_secret,
            tenant_id=tenant_id
        )
        super().__init__(self.credentials)

    def get_recommendations(self) -> list:
        """
        :return: list of recommendations
        """
        logger.info(" ---Inside recommendation :: get_recommendations()--- ")

        response = []

        subscriptions = self.list_subscriptions()

        vm_list = self.list_vms(subscriptions)
        response.extend(self.check_for_ssh_authentication_type(vm_list))
        response.extend(self.disable_premium_ssd(vm_list))
        response.extend(self.enable_auto_shutdown(vm_list))

        disk_list = self.list_disks(subscriptions)
        response.extend(self.remove_unattached_disk_volume(disk_list))

        snapshot_list = self.list_snapshots(subscriptions)
        response.extend(self.remove_old_vm_disk_snapshot(snapshot_list))

        return response


