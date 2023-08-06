from datetime import datetime, timedelta

import pytz
from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class vm_recommendations:
    def __init__(self, credentials: ClientSecretCredential):
        """
        :param credentials: ClientSecretCredential
        """
        self.credentials = credentials

    # provides the recommendation to use ssh authentication type
    def check_for_ssh_authentication_type(self, vm_list: dict) -> list:
        """
        :param vm_list: list of the virtual machine across all the subscriptions
        :return: list of recommendations
        """
        logger.info(" ---Inside vm_recommendations :: disk_encryption_for_boot_disk_volumes()--- ")

        response = []

        for subs, vms in vm_list.items():
            for vm in vms:
                # print(vm)
                # print(vm.storage_profile.os_disk)
                # print(vm.storage_profile.os_disk.managed_disk)
                if vm.os_profile.linux_configuration is not None:
                    if not vm.os_profile.linux_configuration.disable_password_authentication:
                        temp = {
                            'recommendation': 'Use SSH authentication type',
                            'description': 'the SSH authentication type for the selected Microsoft Azure '
                                           'virtual machine is password-based, therefore the SSH authentication '
                                           'method configured for the specified VM is not secure',
                            'resource': 'Virtual Machine',
                            'subscription_id': subs,
                            'resource_id': vm.id,
                            'metadata': {
                                'name': vm.name,
                                'tags': vm.tags
                            }
                        }
                        response.append(temp)

        return response

    # Provides recommendations for removing unattached virtual machine disk volumes
    def remove_unattached_disk_volume(self, disk_list: dict) -> list:
        """
        :param disk_list: list of disks across all the subscriptions
        :return: list of recommendations
        """
        logger.info(" ---Inside vm_recommendations :: remove_unattached_disk_volumes()--- ")

        response = []

        for subscription, disks in disk_list.items():
            for disk in disks:
                # print(disk)
                if disk.disk_state == 'Unattached':
                    temp = {
                        'recommendation': 'Remove unattached disk',
                        'description': 'disk volume is not attached to a Microsoft Azure virtual machine, remove it to optimize the cost',
                        'resource': 'Virtual Machine',
                        'subscription_id': subscription,
                        'resource_id': disk.id,
                        'metadata': {
                            'name': disk.name,
                            'tags': disk.tags
                        }
                    }
                    response.append(temp)

        return response

    # Provides the recommendation for Remove Old Virtual Machine Disk Snapshots
    def remove_old_vm_disk_snapshot(self, snapshot_list: dict) -> list:
        """
        :param snapshot_list: list of snapshots across all subscriptions
        :return: list of recommendations
        """
        logger.info(" ---Inside vm_recommendations :: remove_old_vm_disk_snapshot()--- ")

        response = []

        time_30_days_ago = datetime.now() - timedelta(days=30)
        timezone = pytz.timezone("UTC")
        time_30_days_ago = timezone.localize(time_30_days_ago)

        for subscription, snapshots in snapshot_list.items():
            for snapshot in snapshots:
                time_created = snapshot.time_created
                if time_30_days_ago > time_created:
                    temp = {
                        'recommendation': 'Remove 30 days older vm disk snapshot',
                        'description': 'virtual machine disk snapshot is 30 days old and can be safely removed '
                                       'from your Azure cloud account',
                        'resource': 'Virtual Machine',
                        'subscription_id': subscription,
                        'resource_id': snapshot.id,
                        'metadata': {
                            'name': snapshot.name,
                            'tags': snapshot.tags
                        }
                    }
                    response.append(temp)

        return response

    # Provides the recommendation for disable premium ssd
    def disable_premium_ssd(self, vm_list: dict) -> list:
        """
        :param vm_list: list of Azure Virtual Machines
        :return: list of recommendations
        """
        logger.info(" ---Inside vm_recommendations :: disable_premium_ssd()--- ")

        response = []

        for subscription, vms in vm_list.items():
            for vm in vms:
                os_disk_type = vm.storage_profile.os_disk.managed_disk.storage_account_type
                try:
                    data_disk_type = vm.storage_profile.data_disks.managed_disk.storage_account_type
                    if os_disk_type == 'Premium_LRS' or data_disk_type == 'Premium_LRS':
                        temp = {
                            'recommendation': 'Disable premium SSD',
                            'description': 'Microsoft Azure virtual machines (VMs) are using Premium SSD '
                                           'volumes, use Standard SSD disk volumes for cost-effective storage '
                                           'that fits a broad range of workloads',
                            'resource': 'Virtual Machine',
                            'subscription_id': subscription,
                            'resource_id': vm.id,
                            'metadata': {
                                'name': vm.name,
                                'tags': vm.tags
                            }
                        }
                        response.append(temp)
                except AttributeError:
                    if os_disk_type == 'Premium_LRS':
                        temp = {
                            'recommendation': 'Disable premium SSD',
                            'description': 'Microsoft Azure virtual machines (VMs) are using Premium SSD '
                                           'volumes, use Standard SSD disk volumes for cost-effective storage '
                                           'that fits a broad range of workloads',
                            'resource': 'Virtual Machine',
                            'subscription_id': subscription,
                            'resource_id': vm.id,
                            'metadata': {
                                'name': vm.name,
                                'tags': vm.tags
                            }
                        }
                        response.append(temp)

        return response

    # Provides the recommendation for enable auto-shutdown
    def enable_auto_shutdown(self, vm_list: dict) -> list:
        """
        :param vm_list: list of azure virtual machines
        :return: list of recommendation
        """
        logger.info(" ---vm_recommendations :: enable_auto_shutdown()--- ")

        response = []

        for subscription, vms in vm_list.items():
            resource_client = ResourceManagementClient(credential=self.credentials, subscription_id=subscription)
            for vm in vms:
                auto_shutdown_status = resource_client.resources.get_by_id(vm.id, '2022-11-01').\
                    properties.get('autoShutdownSettings')
                if auto_shutdown_status is None or auto_shutdown_status == 'Disabled':
                    temp = {
                        'recommendation': 'Enable Auto Shutdown',
                        'description': 'Enable Auto Shutdown feature on Microsoft Azure virtual machines (VMs) in '
                                       'order to minimize waste and control VM costs',
                        'resource': 'Virtual Machine',
                        'subscription_id': subscription,
                        'resource_id': vm.id,
                        'metadata': {
                            'name': vm.name,
                            'tags': vm.tags
                        }
                    }
                    response.append(temp)

        return response
