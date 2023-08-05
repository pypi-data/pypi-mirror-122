# coding=utf-8
# *** WARNING: this file was generated by pulumigen. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['ProviderArgs', 'Provider']

@pulumi.input_type
class ProviderArgs:
    def __init__(__self__, *,
                 cluster: Optional[pulumi.Input[str]] = None,
                 context: Optional[pulumi.Input[str]] = None,
                 enable_dry_run: Optional[pulumi.Input[bool]] = None,
                 helm_driver: Optional[pulumi.Input[str]] = None,
                 helm_plugins_path: Optional[pulumi.Input[str]] = None,
                 helm_registry_config_path: Optional[pulumi.Input[str]] = None,
                 helm_repository_cache: Optional[pulumi.Input[str]] = None,
                 helm_repository_config_path: Optional[pulumi.Input[str]] = None,
                 kubeconfig: Optional[pulumi.Input[str]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 render_yaml_to_directory: Optional[pulumi.Input[str]] = None,
                 suppress_deprecation_warnings: Optional[pulumi.Input[bool]] = None,
                 suppress_helm_hook_warnings: Optional[pulumi.Input[bool]] = None,
                 suppress_helm_release_beta_warning: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a Provider resource.
        :param pulumi.Input[str] cluster: If present, the name of the kubeconfig cluster to use.
        :param pulumi.Input[str] context: If present, the name of the kubeconfig context to use.
        :param pulumi.Input[bool] enable_dry_run: BETA FEATURE - If present and set to true, enable server-side diff calculations.
               This feature is in developer preview, and is disabled by default.
        :param pulumi.Input[str] helm_driver: BETA FEATURE - Used for supporting Helm Release resource (Beta). The backend storage driver for Helm. Values are: configmap, secret, memory, sql.
        :param pulumi.Input[str] helm_plugins_path: BETA FEATURE - Used for supporting Helm Release resource (Beta). The path to the helm plugins directory.
        :param pulumi.Input[str] helm_registry_config_path: BETA FEATURE - Used for supporting Helm Release resource (Beta). The path to the registry config file.
        :param pulumi.Input[str] helm_repository_cache: BETA FEATURE - Used for supporting Helm Release resource (Beta). The path to the file containing cached repository indexes.
        :param pulumi.Input[str] helm_repository_config_path: BETA FEATURE - Used for supporting Helm Release resource (Beta). The path to the file containing repository names and URLs.
        :param pulumi.Input[str] kubeconfig: The contents of a kubeconfig file or the path to a kubeconfig file.
        :param pulumi.Input[str] namespace: If present, the default namespace to use. This flag is ignored for cluster-scoped resources.
               
               A namespace can be specified in multiple places, and the precedence is as follows:
               1. `.metadata.namespace` set on the resource.
               2. This `namespace` parameter.
               3. `namespace` set for the active context in the kubeconfig.
        :param pulumi.Input[str] render_yaml_to_directory: BETA FEATURE - If present, render resource manifests to this directory. In this mode, resources will not
               be created on a Kubernetes cluster, but the rendered manifests will be kept in sync with changes
               to the Pulumi program. This feature is in developer preview, and is disabled by default.
               
               Note that some computed Outputs such as status fields will not be populated
               since the resources are not created on a Kubernetes cluster. These Output values will remain undefined,
               and may result in an error if they are referenced by other resources. Also note that any secret values
               used in these resources will be rendered in plaintext to the resulting YAML.
        :param pulumi.Input[bool] suppress_deprecation_warnings: If present and set to true, suppress apiVersion deprecation warnings from the CLI.
        :param pulumi.Input[bool] suppress_helm_hook_warnings: If present and set to true, suppress unsupported Helm hook warnings from the CLI.
        :param pulumi.Input[bool] suppress_helm_release_beta_warning: While Helm Release provider is in beta, by default 'pulumi up' will log a warning if the resource is used. If present and set to "true", this warning is omitted.
        """
        if cluster is not None:
            pulumi.set(__self__, "cluster", cluster)
        if context is not None:
            pulumi.set(__self__, "context", context)
        if enable_dry_run is None:
            enable_dry_run = _utilities.get_env_bool('PULUMI_K8S_ENABLE_DRY_RUN')
        if enable_dry_run is not None:
            pulumi.set(__self__, "enable_dry_run", enable_dry_run)
        if helm_driver is None:
            helm_driver = _utilities.get_env('PULUMI_K8S_HELM_DRIVER')
        if helm_driver is not None:
            pulumi.set(__self__, "helm_driver", helm_driver)
        if helm_plugins_path is None:
            helm_plugins_path = _utilities.get_env('PULUMI_K8S_HELM_PLUGINS_PATH')
        if helm_plugins_path is not None:
            pulumi.set(__self__, "helm_plugins_path", helm_plugins_path)
        if helm_registry_config_path is None:
            helm_registry_config_path = _utilities.get_env('PULUMI_K8S_HELM_REGISTRY_CONFIG_PATH')
        if helm_registry_config_path is not None:
            pulumi.set(__self__, "helm_registry_config_path", helm_registry_config_path)
        if helm_repository_cache is None:
            helm_repository_cache = _utilities.get_env('PULUMI_K8s_HELM_REPOSITORY_CACHE')
        if helm_repository_cache is not None:
            pulumi.set(__self__, "helm_repository_cache", helm_repository_cache)
        if helm_repository_config_path is None:
            helm_repository_config_path = _utilities.get_env('PULUMI_K8S_HELM_REPOSITORY_CONFIG_PATH')
        if helm_repository_config_path is not None:
            pulumi.set(__self__, "helm_repository_config_path", helm_repository_config_path)
        if kubeconfig is None:
            kubeconfig = _utilities.get_env('KUBECONFIG')
        if kubeconfig is not None:
            pulumi.set(__self__, "kubeconfig", kubeconfig)
        if namespace is not None:
            pulumi.set(__self__, "namespace", namespace)
        if render_yaml_to_directory is not None:
            pulumi.set(__self__, "render_yaml_to_directory", render_yaml_to_directory)
        if suppress_deprecation_warnings is None:
            suppress_deprecation_warnings = _utilities.get_env_bool('PULUMI_K8S_SUPPRESS_DEPRECATION_WARNINGS')
        if suppress_deprecation_warnings is not None:
            pulumi.set(__self__, "suppress_deprecation_warnings", suppress_deprecation_warnings)
        if suppress_helm_hook_warnings is None:
            suppress_helm_hook_warnings = _utilities.get_env_bool('PULUMI_K8S_SUPPRESS_HELM_HOOK_WARNINGS')
        if suppress_helm_hook_warnings is not None:
            pulumi.set(__self__, "suppress_helm_hook_warnings", suppress_helm_hook_warnings)
        if suppress_helm_release_beta_warning is None:
            suppress_helm_release_beta_warning = _utilities.get_env_bool('PULUMI_K8S_SUPPRESS_HELM_RELEASE_BETA_WARNING')
        if suppress_helm_release_beta_warning is not None:
            pulumi.set(__self__, "suppress_helm_release_beta_warning", suppress_helm_release_beta_warning)

    @property
    @pulumi.getter
    def cluster(self) -> Optional[pulumi.Input[str]]:
        """
        If present, the name of the kubeconfig cluster to use.
        """
        return pulumi.get(self, "cluster")

    @cluster.setter
    def cluster(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cluster", value)

    @property
    @pulumi.getter
    def context(self) -> Optional[pulumi.Input[str]]:
        """
        If present, the name of the kubeconfig context to use.
        """
        return pulumi.get(self, "context")

    @context.setter
    def context(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "context", value)

    @property
    @pulumi.getter(name="enableDryRun")
    def enable_dry_run(self) -> Optional[pulumi.Input[bool]]:
        """
        BETA FEATURE - If present and set to true, enable server-side diff calculations.
        This feature is in developer preview, and is disabled by default.
        """
        return pulumi.get(self, "enable_dry_run")

    @enable_dry_run.setter
    def enable_dry_run(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_dry_run", value)

    @property
    @pulumi.getter(name="helmDriver")
    def helm_driver(self) -> Optional[pulumi.Input[str]]:
        """
        BETA FEATURE - Used for supporting Helm Release resource (Beta). The backend storage driver for Helm. Values are: configmap, secret, memory, sql.
        """
        return pulumi.get(self, "helm_driver")

    @helm_driver.setter
    def helm_driver(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "helm_driver", value)

    @property
    @pulumi.getter(name="helmPluginsPath")
    def helm_plugins_path(self) -> Optional[pulumi.Input[str]]:
        """
        BETA FEATURE - Used for supporting Helm Release resource (Beta). The path to the helm plugins directory.
        """
        return pulumi.get(self, "helm_plugins_path")

    @helm_plugins_path.setter
    def helm_plugins_path(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "helm_plugins_path", value)

    @property
    @pulumi.getter(name="helmRegistryConfigPath")
    def helm_registry_config_path(self) -> Optional[pulumi.Input[str]]:
        """
        BETA FEATURE - Used for supporting Helm Release resource (Beta). The path to the registry config file.
        """
        return pulumi.get(self, "helm_registry_config_path")

    @helm_registry_config_path.setter
    def helm_registry_config_path(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "helm_registry_config_path", value)

    @property
    @pulumi.getter(name="helmRepositoryCache")
    def helm_repository_cache(self) -> Optional[pulumi.Input[str]]:
        """
        BETA FEATURE - Used for supporting Helm Release resource (Beta). The path to the file containing cached repository indexes.
        """
        return pulumi.get(self, "helm_repository_cache")

    @helm_repository_cache.setter
    def helm_repository_cache(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "helm_repository_cache", value)

    @property
    @pulumi.getter(name="helmRepositoryConfigPath")
    def helm_repository_config_path(self) -> Optional[pulumi.Input[str]]:
        """
        BETA FEATURE - Used for supporting Helm Release resource (Beta). The path to the file containing repository names and URLs.
        """
        return pulumi.get(self, "helm_repository_config_path")

    @helm_repository_config_path.setter
    def helm_repository_config_path(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "helm_repository_config_path", value)

    @property
    @pulumi.getter
    def kubeconfig(self) -> Optional[pulumi.Input[str]]:
        """
        The contents of a kubeconfig file or the path to a kubeconfig file.
        """
        return pulumi.get(self, "kubeconfig")

    @kubeconfig.setter
    def kubeconfig(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kubeconfig", value)

    @property
    @pulumi.getter
    def namespace(self) -> Optional[pulumi.Input[str]]:
        """
        If present, the default namespace to use. This flag is ignored for cluster-scoped resources.

        A namespace can be specified in multiple places, and the precedence is as follows:
        1. `.metadata.namespace` set on the resource.
        2. This `namespace` parameter.
        3. `namespace` set for the active context in the kubeconfig.
        """
        return pulumi.get(self, "namespace")

    @namespace.setter
    def namespace(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "namespace", value)

    @property
    @pulumi.getter(name="renderYamlToDirectory")
    def render_yaml_to_directory(self) -> Optional[pulumi.Input[str]]:
        """
        BETA FEATURE - If present, render resource manifests to this directory. In this mode, resources will not
        be created on a Kubernetes cluster, but the rendered manifests will be kept in sync with changes
        to the Pulumi program. This feature is in developer preview, and is disabled by default.

        Note that some computed Outputs such as status fields will not be populated
        since the resources are not created on a Kubernetes cluster. These Output values will remain undefined,
        and may result in an error if they are referenced by other resources. Also note that any secret values
        used in these resources will be rendered in plaintext to the resulting YAML.
        """
        return pulumi.get(self, "render_yaml_to_directory")

    @render_yaml_to_directory.setter
    def render_yaml_to_directory(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "render_yaml_to_directory", value)

    @property
    @pulumi.getter(name="suppressDeprecationWarnings")
    def suppress_deprecation_warnings(self) -> Optional[pulumi.Input[bool]]:
        """
        If present and set to true, suppress apiVersion deprecation warnings from the CLI.
        """
        return pulumi.get(self, "suppress_deprecation_warnings")

    @suppress_deprecation_warnings.setter
    def suppress_deprecation_warnings(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "suppress_deprecation_warnings", value)

    @property
    @pulumi.getter(name="suppressHelmHookWarnings")
    def suppress_helm_hook_warnings(self) -> Optional[pulumi.Input[bool]]:
        """
        If present and set to true, suppress unsupported Helm hook warnings from the CLI.
        """
        return pulumi.get(self, "suppress_helm_hook_warnings")

    @suppress_helm_hook_warnings.setter
    def suppress_helm_hook_warnings(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "suppress_helm_hook_warnings", value)

    @property
    @pulumi.getter(name="suppressHelmReleaseBetaWarning")
    def suppress_helm_release_beta_warning(self) -> Optional[pulumi.Input[bool]]:
        """
        While Helm Release provider is in beta, by default 'pulumi up' will log a warning if the resource is used. If present and set to "true", this warning is omitted.
        """
        return pulumi.get(self, "suppress_helm_release_beta_warning")

    @suppress_helm_release_beta_warning.setter
    def suppress_helm_release_beta_warning(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "suppress_helm_release_beta_warning", value)


class Provider(pulumi.ProviderResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cluster: Optional[pulumi.Input[str]] = None,
                 context: Optional[pulumi.Input[str]] = None,
                 enable_dry_run: Optional[pulumi.Input[bool]] = None,
                 helm_driver: Optional[pulumi.Input[str]] = None,
                 helm_plugins_path: Optional[pulumi.Input[str]] = None,
                 helm_registry_config_path: Optional[pulumi.Input[str]] = None,
                 helm_repository_cache: Optional[pulumi.Input[str]] = None,
                 helm_repository_config_path: Optional[pulumi.Input[str]] = None,
                 kubeconfig: Optional[pulumi.Input[str]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 render_yaml_to_directory: Optional[pulumi.Input[str]] = None,
                 suppress_deprecation_warnings: Optional[pulumi.Input[bool]] = None,
                 suppress_helm_hook_warnings: Optional[pulumi.Input[bool]] = None,
                 suppress_helm_release_beta_warning: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        """
        The provider type for the kubernetes package.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cluster: If present, the name of the kubeconfig cluster to use.
        :param pulumi.Input[str] context: If present, the name of the kubeconfig context to use.
        :param pulumi.Input[bool] enable_dry_run: BETA FEATURE - If present and set to true, enable server-side diff calculations.
               This feature is in developer preview, and is disabled by default.
        :param pulumi.Input[str] helm_driver: BETA FEATURE - Used for supporting Helm Release resource (Beta). The backend storage driver for Helm. Values are: configmap, secret, memory, sql.
        :param pulumi.Input[str] helm_plugins_path: BETA FEATURE - Used for supporting Helm Release resource (Beta). The path to the helm plugins directory.
        :param pulumi.Input[str] helm_registry_config_path: BETA FEATURE - Used for supporting Helm Release resource (Beta). The path to the registry config file.
        :param pulumi.Input[str] helm_repository_cache: BETA FEATURE - Used for supporting Helm Release resource (Beta). The path to the file containing cached repository indexes.
        :param pulumi.Input[str] helm_repository_config_path: BETA FEATURE - Used for supporting Helm Release resource (Beta). The path to the file containing repository names and URLs.
        :param pulumi.Input[str] kubeconfig: The contents of a kubeconfig file or the path to a kubeconfig file.
        :param pulumi.Input[str] namespace: If present, the default namespace to use. This flag is ignored for cluster-scoped resources.
               
               A namespace can be specified in multiple places, and the precedence is as follows:
               1. `.metadata.namespace` set on the resource.
               2. This `namespace` parameter.
               3. `namespace` set for the active context in the kubeconfig.
        :param pulumi.Input[str] render_yaml_to_directory: BETA FEATURE - If present, render resource manifests to this directory. In this mode, resources will not
               be created on a Kubernetes cluster, but the rendered manifests will be kept in sync with changes
               to the Pulumi program. This feature is in developer preview, and is disabled by default.
               
               Note that some computed Outputs such as status fields will not be populated
               since the resources are not created on a Kubernetes cluster. These Output values will remain undefined,
               and may result in an error if they are referenced by other resources. Also note that any secret values
               used in these resources will be rendered in plaintext to the resulting YAML.
        :param pulumi.Input[bool] suppress_deprecation_warnings: If present and set to true, suppress apiVersion deprecation warnings from the CLI.
        :param pulumi.Input[bool] suppress_helm_hook_warnings: If present and set to true, suppress unsupported Helm hook warnings from the CLI.
        :param pulumi.Input[bool] suppress_helm_release_beta_warning: While Helm Release provider is in beta, by default 'pulumi up' will log a warning if the resource is used. If present and set to "true", this warning is omitted.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[ProviderArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The provider type for the kubernetes package.

        :param str resource_name: The name of the resource.
        :param ProviderArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ProviderArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cluster: Optional[pulumi.Input[str]] = None,
                 context: Optional[pulumi.Input[str]] = None,
                 enable_dry_run: Optional[pulumi.Input[bool]] = None,
                 helm_driver: Optional[pulumi.Input[str]] = None,
                 helm_plugins_path: Optional[pulumi.Input[str]] = None,
                 helm_registry_config_path: Optional[pulumi.Input[str]] = None,
                 helm_repository_cache: Optional[pulumi.Input[str]] = None,
                 helm_repository_config_path: Optional[pulumi.Input[str]] = None,
                 kubeconfig: Optional[pulumi.Input[str]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 render_yaml_to_directory: Optional[pulumi.Input[str]] = None,
                 suppress_deprecation_warnings: Optional[pulumi.Input[bool]] = None,
                 suppress_helm_hook_warnings: Optional[pulumi.Input[bool]] = None,
                 suppress_helm_release_beta_warning: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ProviderArgs.__new__(ProviderArgs)

            __props__.__dict__["cluster"] = cluster
            __props__.__dict__["context"] = context
            if enable_dry_run is None:
                enable_dry_run = _utilities.get_env_bool('PULUMI_K8S_ENABLE_DRY_RUN')
            __props__.__dict__["enable_dry_run"] = pulumi.Output.from_input(enable_dry_run).apply(pulumi.runtime.to_json) if enable_dry_run is not None else None
            if helm_driver is None:
                helm_driver = _utilities.get_env('PULUMI_K8S_HELM_DRIVER')
            __props__.__dict__["helm_driver"] = helm_driver
            if helm_plugins_path is None:
                helm_plugins_path = _utilities.get_env('PULUMI_K8S_HELM_PLUGINS_PATH')
            __props__.__dict__["helm_plugins_path"] = helm_plugins_path
            if helm_registry_config_path is None:
                helm_registry_config_path = _utilities.get_env('PULUMI_K8S_HELM_REGISTRY_CONFIG_PATH')
            __props__.__dict__["helm_registry_config_path"] = helm_registry_config_path
            if helm_repository_cache is None:
                helm_repository_cache = _utilities.get_env('PULUMI_K8s_HELM_REPOSITORY_CACHE')
            __props__.__dict__["helm_repository_cache"] = helm_repository_cache
            if helm_repository_config_path is None:
                helm_repository_config_path = _utilities.get_env('PULUMI_K8S_HELM_REPOSITORY_CONFIG_PATH')
            __props__.__dict__["helm_repository_config_path"] = helm_repository_config_path
            if kubeconfig is None:
                kubeconfig = _utilities.get_env('KUBECONFIG')
            __props__.__dict__["kubeconfig"] = kubeconfig
            __props__.__dict__["namespace"] = namespace
            __props__.__dict__["render_yaml_to_directory"] = render_yaml_to_directory
            if suppress_deprecation_warnings is None:
                suppress_deprecation_warnings = _utilities.get_env_bool('PULUMI_K8S_SUPPRESS_DEPRECATION_WARNINGS')
            __props__.__dict__["suppress_deprecation_warnings"] = pulumi.Output.from_input(suppress_deprecation_warnings).apply(pulumi.runtime.to_json) if suppress_deprecation_warnings is not None else None
            if suppress_helm_hook_warnings is None:
                suppress_helm_hook_warnings = _utilities.get_env_bool('PULUMI_K8S_SUPPRESS_HELM_HOOK_WARNINGS')
            __props__.__dict__["suppress_helm_hook_warnings"] = pulumi.Output.from_input(suppress_helm_hook_warnings).apply(pulumi.runtime.to_json) if suppress_helm_hook_warnings is not None else None
            if suppress_helm_release_beta_warning is None:
                suppress_helm_release_beta_warning = _utilities.get_env_bool('PULUMI_K8S_SUPPRESS_HELM_RELEASE_BETA_WARNING')
            __props__.__dict__["suppress_helm_release_beta_warning"] = pulumi.Output.from_input(suppress_helm_release_beta_warning).apply(pulumi.runtime.to_json) if suppress_helm_release_beta_warning is not None else None
        super(Provider, __self__).__init__(
            'kubernetes',
            resource_name,
            __props__,
            opts)

