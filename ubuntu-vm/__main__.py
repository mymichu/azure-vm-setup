import pulumi
import pulumi_azure_native as azure_native
from pulumi_azure_native import resources
import base64
import pathlib

username="michel"

# Create an Azure Resource Group
resource_group = resources.ResourceGroup("ubuntu-vm")

net = azure_native.network.VirtualNetwork(
    "server-network",
    resource_group_name=resource_group.name,
    address_space=azure_native.network.AddressSpaceArgs(
        address_prefixes=["10.0.0.0/16"],
    ),
    subnets=[azure_native.network.SubnetArgs(
        name="default",
        address_prefix="10.0.1.0/24",
    )])


public_ip = azure_native.network.PublicIPAddress(
    "server-ip",
    resource_group_name=resource_group.name,
    public_ip_allocation_method=azure_native.network.IPAllocationMethod.DYNAMIC)

network_iface = azure_native.network.NetworkInterface(
    "server-nic",
    resource_group_name=resource_group.name,
    ip_configurations=[azure_native.network.NetworkInterfaceIPConfigurationArgs(
        name="vmservercfg",
        subnet=azure_native.network.SubnetArgs(id=net.subnets[0].id),
        private_ip_allocation_method=azure_native.network.IPAllocationMethod.DYNAMIC,
        public_ip_address=azure_native.network.PublicIPAddressArgs(id=public_ip.id),
    )])

current_dir = pathlib.Path(__file__).parent.resolve()
data = open(f"{current_dir}/cloud-init.yml", "r").read()
utf8_code = data.encode("UTF-8")
encoded_cloud_init = base64.b64encode(utf8_code)

virtual_machine = azure_native.compute.VirtualMachine("virtualMachine",
    hardware_profile=azure_native.compute.HardwareProfileArgs(
        vm_size="Standard_D1_v2",
    ),
    location="australiasoutheast",
    network_profile=azure_native.compute.NetworkProfileArgs(
        network_interfaces=[azure_native.compute.NetworkInterfaceReferenceArgs(
            id=network_iface.id,
            primary=True,
        )],
    ),
    

    os_profile=azure_native.compute.OSProfileArgs(
        admin_username=f"{username}",
        computer_name="myVM",
        linux_configuration=azure_native.compute.LinuxConfigurationArgs(
            disable_password_authentication=True,
            ssh=azure_native.compute.SshConfigurationArgs(
                public_keys=[azure_native.compute.SshPublicKeyArgs(
                    key_data="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQD31EM32A2rlYJp+PIj1+8DgLkMYrbgfoh06HUP6eEEWnItQNJTu5AnN8RlYvIDwIbunK7caOU7mxm74/jjYAK42pAOxCjR43WdgiUH+RWcfIUG8wN01obzr6MKQwhCNS6Z+lNWd4oThr9+vfUL93GlAFZWXI4J9g/dSdnS8Tf25sRglPH5GtG7+mgJPTToeAtIupMVYFFudPoRtMza4Kf2PeEfq5nNxSAI8Xbq/KYwDprJkeusza/tAo+HQeUiYJTxVdi/2k6mlQx/xoc7ZWG4x+0ydRz/OATCkpYqyykDIesQePLrN7KaL5ch1dQJmbjIF4jB5c4TK1nn5Jsn/IjUEwsoZP2LzDGKnpVtUy1ZXO9Zp4xwivw84WUhGyV98fB7ozYopRjJ3tWUBLGJI+DZR6TsK9GNVDTuLpwxwue6Z8luFZFwAzBMTeRAwi/PDxOmhnFi9+f/WB0wbZ1isyT5Jih3MvnXAkZ17NcNjRjm2RdO4knumpev3N7xSNazogE= michel@michel-Precision-5550",
                    path=f"/home/{username}/.ssh/authorized_keys",
                )],
            ),
        ),
        custom_data=encoded_cloud_init.decode("utf-8")
    ),
    resource_group_name=resource_group.name,
    storage_profile=azure_native.compute.StorageProfileArgs(
        image_reference=azure_native.compute.ImageReferenceArgs(
            offer="UbuntuServer",
            publisher="Canonical",
            sku="18.04-LTS",
            version="latest",
        ),
        os_disk=azure_native.compute.OSDiskArgs(
            caching="ReadWrite",
            create_option="FromImage",
            managed_disk=azure_native.compute.ManagedDiskParametersArgs(
                storage_account_type="Standard_LRS",
            ),
            name="myVMosdisk",
        ),
    ),
    vm_name="myVM")