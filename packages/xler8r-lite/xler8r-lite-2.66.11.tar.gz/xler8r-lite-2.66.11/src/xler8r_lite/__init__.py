'''
# XLER8R Patterns

XLER8R Patterns are designed to fast track most commonly used architectures, while XLER8R Lite supports provisioning
for static web hosting infrastructure only, XLER8R premium provides support for building serverless APIs, container based
applications, organizational hierarchy setup, sso setup, management account and member account setup and many more.
Reach out to info@cre8ivelogix.com to find out more about premium version of XLER8R https://xler8r.com

## Create a CDK project

To try out XLER8R Lite by itself you can create a new CDK project by running the following commands

```shell
cdk init app --language typescript
```

This will create a bare bone CDK project.

## Adding WA-CDK Lite dependency

Open CDK project in your favorite IDE, goto package.json file and add the WA-CDK-Lite dependency

```json
{
   "dependencies": {
      "@cre8ivelogix/xler8r-lite": "CURRENT_VERSION"
   }
}
```

## Install Dependencies

Once package.json file is updated, you can install the dependencies by running the following commands

```shell
npm install
```

## Using Well Architected CDK constructs

Now that you have all the constructs available from XLER8R Lite,
use them just like any other class in typescript.

For example in the following code snippet we are using WaBucket from AWS-CDK-Lite package

```python
 new X8Website(this, "TestWebSite", {
    waDomainName: 'example.com',
});
```

The Bucket created using WaBucket by default satisfies various security and compliance requirements,
checkout WaBucket class documentation for details.

### Well Architected CDK Version Updates

The version of all CDK packages are fixed to the same version. If an
upgrade is desired, please make sure that all CDK packages are upgraded
to the same version at the same time. Different versions of CDK mixed
in the project may cause type incompatibilities.

### Useful commands

* `npm run build` compile typescript to js
* `npm run watch` watch for changes and compile
* `npm run test` perform the jest unit tests
* `npm run build-test` builds and runs unit tests
* `npm run doc-gen` generate documentation
* `npm run pretty` runs prettier on source code
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk.aws_cloudfront as _aws_cdk_aws_cloudfront_ceddda9d
import constructs as _constructs_77d1e7e8
import wa_cdk_lite as _wa_cdk_lite_597004ae


@jsii.data_type(
    jsii_type="@cre8ivelogix/xler8r-lite.X8WebSiteProps",
    jsii_struct_bases=[],
    name_mapping={
        "wa_domain_name": "waDomainName",
        "wa_additional_domain_names": "waAdditionalDomainNames",
        "wa_bucket_policy_actions": "waBucketPolicyActions",
        "wa_bucket_props": "waBucketProps",
        "wa_cloud_front_distribution_default_behavior": "waCloudFrontDistributionDefaultBehavior",
        "wa_default_root_object": "waDefaultRootObject",
        "wa_enable_cloud_front_logging": "waEnableCloudFrontLogging",
        "wa_error_response_page_path": "waErrorResponsePagePath",
        "wa_origin_access_identity": "waOriginAccessIdentity",
        "wa_path_to_content": "waPathToContent",
        "wa_sub_domain": "waSubDomain",
    },
)
class X8WebSiteProps:
    def __init__(
        self,
        *,
        wa_domain_name: builtins.str,
        wa_additional_domain_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        wa_bucket_policy_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        wa_bucket_props: typing.Optional[typing.Union[_wa_cdk_lite_597004ae.WaBucketProps, typing.Dict[builtins.str, typing.Any]]] = None,
        wa_cloud_front_distribution_default_behavior: typing.Optional[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.BehaviorOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        wa_default_root_object: typing.Optional[builtins.str] = None,
        wa_enable_cloud_front_logging: typing.Optional[builtins.bool] = None,
        wa_error_response_page_path: typing.Optional[builtins.str] = None,
        wa_origin_access_identity: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.OriginAccessIdentity] = None,
        wa_path_to_content: typing.Optional[builtins.str] = None,
        wa_sub_domain: typing.Optional[builtins.str] = None,
    ) -> None:
        '''X8WebSiteProps can be used to configure several behaviors of the hosted website.

        :param wa_domain_name: This property is used to provide the domain name where the website will be hosted.
        :param wa_additional_domain_names: Additional domain names to be included in ssl and redirect traffic to main domain.
        :param wa_bucket_policy_actions: This property is used to provide any additional bucket policies actions. Default: s3:GetObject
        :param wa_bucket_props: This property is used to override existing or provide additional properties for bucket configuration.
        :param wa_cloud_front_distribution_default_behavior: This property is used to override the cloudfront distribution behavior.
        :param wa_default_root_object: This property is used to provide custom root object for the cloudfront distribution. Default: index.html
        :param wa_enable_cloud_front_logging: This property is used to disable or enable cloudfront logging. Default: false
        :param wa_error_response_page_path: This property is used to provide custom error page for the cloudfront distribution. Path must begin with / Default: /error.html
        :param wa_origin_access_identity: This property is used to provide existing origin access identity instead of creating a new one.
        :param wa_path_to_content: This property is used to provide the site content. Default: build
        :param wa_sub_domain: This property is used to provide the subdomain name where the website will be hosted. Default: www
        '''
        if isinstance(wa_bucket_props, dict):
            wa_bucket_props = _wa_cdk_lite_597004ae.WaBucketProps(**wa_bucket_props)
        if isinstance(wa_cloud_front_distribution_default_behavior, dict):
            wa_cloud_front_distribution_default_behavior = _aws_cdk_aws_cloudfront_ceddda9d.BehaviorOptions(**wa_cloud_front_distribution_default_behavior)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eef911c1fc2e9a12bd4f860fa566b7374a8ba5582d3a6a483773f671385807ec)
            check_type(argname="argument wa_domain_name", value=wa_domain_name, expected_type=type_hints["wa_domain_name"])
            check_type(argname="argument wa_additional_domain_names", value=wa_additional_domain_names, expected_type=type_hints["wa_additional_domain_names"])
            check_type(argname="argument wa_bucket_policy_actions", value=wa_bucket_policy_actions, expected_type=type_hints["wa_bucket_policy_actions"])
            check_type(argname="argument wa_bucket_props", value=wa_bucket_props, expected_type=type_hints["wa_bucket_props"])
            check_type(argname="argument wa_cloud_front_distribution_default_behavior", value=wa_cloud_front_distribution_default_behavior, expected_type=type_hints["wa_cloud_front_distribution_default_behavior"])
            check_type(argname="argument wa_default_root_object", value=wa_default_root_object, expected_type=type_hints["wa_default_root_object"])
            check_type(argname="argument wa_enable_cloud_front_logging", value=wa_enable_cloud_front_logging, expected_type=type_hints["wa_enable_cloud_front_logging"])
            check_type(argname="argument wa_error_response_page_path", value=wa_error_response_page_path, expected_type=type_hints["wa_error_response_page_path"])
            check_type(argname="argument wa_origin_access_identity", value=wa_origin_access_identity, expected_type=type_hints["wa_origin_access_identity"])
            check_type(argname="argument wa_path_to_content", value=wa_path_to_content, expected_type=type_hints["wa_path_to_content"])
            check_type(argname="argument wa_sub_domain", value=wa_sub_domain, expected_type=type_hints["wa_sub_domain"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "wa_domain_name": wa_domain_name,
        }
        if wa_additional_domain_names is not None:
            self._values["wa_additional_domain_names"] = wa_additional_domain_names
        if wa_bucket_policy_actions is not None:
            self._values["wa_bucket_policy_actions"] = wa_bucket_policy_actions
        if wa_bucket_props is not None:
            self._values["wa_bucket_props"] = wa_bucket_props
        if wa_cloud_front_distribution_default_behavior is not None:
            self._values["wa_cloud_front_distribution_default_behavior"] = wa_cloud_front_distribution_default_behavior
        if wa_default_root_object is not None:
            self._values["wa_default_root_object"] = wa_default_root_object
        if wa_enable_cloud_front_logging is not None:
            self._values["wa_enable_cloud_front_logging"] = wa_enable_cloud_front_logging
        if wa_error_response_page_path is not None:
            self._values["wa_error_response_page_path"] = wa_error_response_page_path
        if wa_origin_access_identity is not None:
            self._values["wa_origin_access_identity"] = wa_origin_access_identity
        if wa_path_to_content is not None:
            self._values["wa_path_to_content"] = wa_path_to_content
        if wa_sub_domain is not None:
            self._values["wa_sub_domain"] = wa_sub_domain

    @builtins.property
    def wa_domain_name(self) -> builtins.str:
        '''This property is used to provide the domain name where the website will be hosted.'''
        result = self._values.get("wa_domain_name")
        assert result is not None, "Required property 'wa_domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def wa_additional_domain_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Additional domain names to be included in ssl and redirect traffic to main domain.'''
        result = self._values.get("wa_additional_domain_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def wa_bucket_policy_actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''This property is used to provide any additional bucket policies actions.

        :default: s3:GetObject
        '''
        result = self._values.get("wa_bucket_policy_actions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def wa_bucket_props(self) -> typing.Optional[_wa_cdk_lite_597004ae.WaBucketProps]:
        '''This property is used to override existing or provide additional properties for bucket configuration.'''
        result = self._values.get("wa_bucket_props")
        return typing.cast(typing.Optional[_wa_cdk_lite_597004ae.WaBucketProps], result)

    @builtins.property
    def wa_cloud_front_distribution_default_behavior(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.BehaviorOptions]:
        '''This property is used to override the cloudfront distribution behavior.'''
        result = self._values.get("wa_cloud_front_distribution_default_behavior")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.BehaviorOptions], result)

    @builtins.property
    def wa_default_root_object(self) -> typing.Optional[builtins.str]:
        '''This property is used to provide custom root object for the cloudfront distribution.

        :default: index.html
        '''
        result = self._values.get("wa_default_root_object")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def wa_enable_cloud_front_logging(self) -> typing.Optional[builtins.bool]:
        '''This property is used to disable or enable cloudfront logging.

        :default: false
        '''
        result = self._values.get("wa_enable_cloud_front_logging")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def wa_error_response_page_path(self) -> typing.Optional[builtins.str]:
        '''This property is used to provide custom error page for the cloudfront distribution.

        Path must begin with /

        :default: /error.html
        '''
        result = self._values.get("wa_error_response_page_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def wa_origin_access_identity(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.OriginAccessIdentity]:
        '''This property is used to provide existing origin access identity instead of creating a new one.'''
        result = self._values.get("wa_origin_access_identity")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.OriginAccessIdentity], result)

    @builtins.property
    def wa_path_to_content(self) -> typing.Optional[builtins.str]:
        '''This property is used to provide the site content.

        :default: build
        '''
        result = self._values.get("wa_path_to_content")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def wa_sub_domain(self) -> typing.Optional[builtins.str]:
        '''This property is used to provide the subdomain name where the website will be hosted.

        :default: www
        '''
        result = self._values.get("wa_sub_domain")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "X8WebSiteProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class X8Website(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cre8ivelogix/xler8r-lite.X8Website",
):
    '''This construct can help build Well Architected infrastructure for website hosting in AWS using S3 Bucket It will create the following Well Architected resources using CRE8IVELOGIX Well Architected CDK Lite as part of the infrastructure 1.

    A validated public certificate for the website domain
    2. An S3 Bucket using Well Architected Bucket construct
    3. Creates and attaches the Bucket policies
    4. A CloudFront distribution for bucket origin
    7. A Route53 record to route traffic to CloudFront Distribution
    8. Deploys the website content to the bucket


    Default Alarms

    ###Examples
    Default Usage Example::

       new X8Website(this, "LogicalId", {
             waDomainName: 'cre8ivelogix.com',
             waSubdomain: "www",
             waPathToContent: './site-content'
       });

    Custom Configuration Example::

       new X8Website(this, "LogicalId", {
             waDomainName: 'cre8ivelogix.com',
             waSubdomain: "www",
             waPathToContent: './site-content',
             waAdditionalDomainNames: ['www2.cre8ivelogix.com']
       });


    Compliance

    It addresses the following compliance requirements

    - Enable Origin Access Identity for Distributions with S3 Origin
    - Use CloudFront Content Distribution Network
    - Enable S3 Block Public Access for S3 Buckets
    - Enable S3 Bucket Keys
    - Secure Transport
    - Server Side Encryption
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        name: builtins.str,
        *,
        wa_domain_name: builtins.str,
        wa_additional_domain_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        wa_bucket_policy_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        wa_bucket_props: typing.Optional[typing.Union[_wa_cdk_lite_597004ae.WaBucketProps, typing.Dict[builtins.str, typing.Any]]] = None,
        wa_cloud_front_distribution_default_behavior: typing.Optional[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.BehaviorOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        wa_default_root_object: typing.Optional[builtins.str] = None,
        wa_enable_cloud_front_logging: typing.Optional[builtins.bool] = None,
        wa_error_response_page_path: typing.Optional[builtins.str] = None,
        wa_origin_access_identity: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.OriginAccessIdentity] = None,
        wa_path_to_content: typing.Optional[builtins.str] = None,
        wa_sub_domain: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param name: -
        :param wa_domain_name: This property is used to provide the domain name where the website will be hosted.
        :param wa_additional_domain_names: Additional domain names to be included in ssl and redirect traffic to main domain.
        :param wa_bucket_policy_actions: This property is used to provide any additional bucket policies actions. Default: s3:GetObject
        :param wa_bucket_props: This property is used to override existing or provide additional properties for bucket configuration.
        :param wa_cloud_front_distribution_default_behavior: This property is used to override the cloudfront distribution behavior.
        :param wa_default_root_object: This property is used to provide custom root object for the cloudfront distribution. Default: index.html
        :param wa_enable_cloud_front_logging: This property is used to disable or enable cloudfront logging. Default: false
        :param wa_error_response_page_path: This property is used to provide custom error page for the cloudfront distribution. Path must begin with / Default: /error.html
        :param wa_origin_access_identity: This property is used to provide existing origin access identity instead of creating a new one.
        :param wa_path_to_content: This property is used to provide the site content. Default: build
        :param wa_sub_domain: This property is used to provide the subdomain name where the website will be hosted. Default: www
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0fdea107373c62979d68a3dd6a36b3e12af38f9207c537b8977b8f035572f59)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        props = X8WebSiteProps(
            wa_domain_name=wa_domain_name,
            wa_additional_domain_names=wa_additional_domain_names,
            wa_bucket_policy_actions=wa_bucket_policy_actions,
            wa_bucket_props=wa_bucket_props,
            wa_cloud_front_distribution_default_behavior=wa_cloud_front_distribution_default_behavior,
            wa_default_root_object=wa_default_root_object,
            wa_enable_cloud_front_logging=wa_enable_cloud_front_logging,
            wa_error_response_page_path=wa_error_response_page_path,
            wa_origin_access_identity=wa_origin_access_identity,
            wa_path_to_content=wa_path_to_content,
            wa_sub_domain=wa_sub_domain,
        )

        jsii.create(self.__class__, self, [scope, name, props])

    @jsii.member(jsii_name="domainNameToPascalCase")
    @builtins.classmethod
    def domain_name_to_pascal_case(cls, domain_name: builtins.str) -> builtins.str:
        '''
        :param domain_name: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c33cc3dfd199fa875209f2b95becc7fa167f83beb6362ad61fd5c9639d074b73)
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "domainNameToPascalCase", [domain_name]))

    @jsii.member(jsii_name="getCertificateDomains")
    def get_certificate_domains(
        self,
        *,
        wa_domain_name: builtins.str,
        wa_additional_domain_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        wa_bucket_policy_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        wa_bucket_props: typing.Optional[typing.Union[_wa_cdk_lite_597004ae.WaBucketProps, typing.Dict[builtins.str, typing.Any]]] = None,
        wa_cloud_front_distribution_default_behavior: typing.Optional[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.BehaviorOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        wa_default_root_object: typing.Optional[builtins.str] = None,
        wa_enable_cloud_front_logging: typing.Optional[builtins.bool] = None,
        wa_error_response_page_path: typing.Optional[builtins.str] = None,
        wa_origin_access_identity: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.OriginAccessIdentity] = None,
        wa_path_to_content: typing.Optional[builtins.str] = None,
        wa_sub_domain: typing.Optional[builtins.str] = None,
    ) -> typing.List[builtins.str]:
        '''
        :param wa_domain_name: This property is used to provide the domain name where the website will be hosted.
        :param wa_additional_domain_names: Additional domain names to be included in ssl and redirect traffic to main domain.
        :param wa_bucket_policy_actions: This property is used to provide any additional bucket policies actions. Default: s3:GetObject
        :param wa_bucket_props: This property is used to override existing or provide additional properties for bucket configuration.
        :param wa_cloud_front_distribution_default_behavior: This property is used to override the cloudfront distribution behavior.
        :param wa_default_root_object: This property is used to provide custom root object for the cloudfront distribution. Default: index.html
        :param wa_enable_cloud_front_logging: This property is used to disable or enable cloudfront logging. Default: false
        :param wa_error_response_page_path: This property is used to provide custom error page for the cloudfront distribution. Path must begin with / Default: /error.html
        :param wa_origin_access_identity: This property is used to provide existing origin access identity instead of creating a new one.
        :param wa_path_to_content: This property is used to provide the site content. Default: build
        :param wa_sub_domain: This property is used to provide the subdomain name where the website will be hosted. Default: www
        '''
        props = X8WebSiteProps(
            wa_domain_name=wa_domain_name,
            wa_additional_domain_names=wa_additional_domain_names,
            wa_bucket_policy_actions=wa_bucket_policy_actions,
            wa_bucket_props=wa_bucket_props,
            wa_cloud_front_distribution_default_behavior=wa_cloud_front_distribution_default_behavior,
            wa_default_root_object=wa_default_root_object,
            wa_enable_cloud_front_logging=wa_enable_cloud_front_logging,
            wa_error_response_page_path=wa_error_response_page_path,
            wa_origin_access_identity=wa_origin_access_identity,
            wa_path_to_content=wa_path_to_content,
            wa_sub_domain=wa_sub_domain,
        )

        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "getCertificateDomains", [props]))

    @jsii.member(jsii_name="getDistributionDomains")
    def get_distribution_domains(
        self,
        *,
        wa_domain_name: builtins.str,
        wa_additional_domain_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        wa_bucket_policy_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        wa_bucket_props: typing.Optional[typing.Union[_wa_cdk_lite_597004ae.WaBucketProps, typing.Dict[builtins.str, typing.Any]]] = None,
        wa_cloud_front_distribution_default_behavior: typing.Optional[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.BehaviorOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        wa_default_root_object: typing.Optional[builtins.str] = None,
        wa_enable_cloud_front_logging: typing.Optional[builtins.bool] = None,
        wa_error_response_page_path: typing.Optional[builtins.str] = None,
        wa_origin_access_identity: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.OriginAccessIdentity] = None,
        wa_path_to_content: typing.Optional[builtins.str] = None,
        wa_sub_domain: typing.Optional[builtins.str] = None,
    ) -> typing.List[builtins.str]:
        '''
        :param wa_domain_name: This property is used to provide the domain name where the website will be hosted.
        :param wa_additional_domain_names: Additional domain names to be included in ssl and redirect traffic to main domain.
        :param wa_bucket_policy_actions: This property is used to provide any additional bucket policies actions. Default: s3:GetObject
        :param wa_bucket_props: This property is used to override existing or provide additional properties for bucket configuration.
        :param wa_cloud_front_distribution_default_behavior: This property is used to override the cloudfront distribution behavior.
        :param wa_default_root_object: This property is used to provide custom root object for the cloudfront distribution. Default: index.html
        :param wa_enable_cloud_front_logging: This property is used to disable or enable cloudfront logging. Default: false
        :param wa_error_response_page_path: This property is used to provide custom error page for the cloudfront distribution. Path must begin with / Default: /error.html
        :param wa_origin_access_identity: This property is used to provide existing origin access identity instead of creating a new one.
        :param wa_path_to_content: This property is used to provide the site content. Default: build
        :param wa_sub_domain: This property is used to provide the subdomain name where the website will be hosted. Default: www
        '''
        props = X8WebSiteProps(
            wa_domain_name=wa_domain_name,
            wa_additional_domain_names=wa_additional_domain_names,
            wa_bucket_policy_actions=wa_bucket_policy_actions,
            wa_bucket_props=wa_bucket_props,
            wa_cloud_front_distribution_default_behavior=wa_cloud_front_distribution_default_behavior,
            wa_default_root_object=wa_default_root_object,
            wa_enable_cloud_front_logging=wa_enable_cloud_front_logging,
            wa_error_response_page_path=wa_error_response_page_path,
            wa_origin_access_identity=wa_origin_access_identity,
            wa_path_to_content=wa_path_to_content,
            wa_sub_domain=wa_sub_domain,
        )

        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "getDistributionDomains", [props]))

    @jsii.member(jsii_name="getSiteDomain")
    def get_site_domain(
        self,
        *,
        wa_domain_name: builtins.str,
        wa_additional_domain_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        wa_bucket_policy_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        wa_bucket_props: typing.Optional[typing.Union[_wa_cdk_lite_597004ae.WaBucketProps, typing.Dict[builtins.str, typing.Any]]] = None,
        wa_cloud_front_distribution_default_behavior: typing.Optional[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.BehaviorOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        wa_default_root_object: typing.Optional[builtins.str] = None,
        wa_enable_cloud_front_logging: typing.Optional[builtins.bool] = None,
        wa_error_response_page_path: typing.Optional[builtins.str] = None,
        wa_origin_access_identity: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.OriginAccessIdentity] = None,
        wa_path_to_content: typing.Optional[builtins.str] = None,
        wa_sub_domain: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        '''
        :param wa_domain_name: This property is used to provide the domain name where the website will be hosted.
        :param wa_additional_domain_names: Additional domain names to be included in ssl and redirect traffic to main domain.
        :param wa_bucket_policy_actions: This property is used to provide any additional bucket policies actions. Default: s3:GetObject
        :param wa_bucket_props: This property is used to override existing or provide additional properties for bucket configuration.
        :param wa_cloud_front_distribution_default_behavior: This property is used to override the cloudfront distribution behavior.
        :param wa_default_root_object: This property is used to provide custom root object for the cloudfront distribution. Default: index.html
        :param wa_enable_cloud_front_logging: This property is used to disable or enable cloudfront logging. Default: false
        :param wa_error_response_page_path: This property is used to provide custom error page for the cloudfront distribution. Path must begin with / Default: /error.html
        :param wa_origin_access_identity: This property is used to provide existing origin access identity instead of creating a new one.
        :param wa_path_to_content: This property is used to provide the site content. Default: build
        :param wa_sub_domain: This property is used to provide the subdomain name where the website will be hosted. Default: www
        '''
        props = X8WebSiteProps(
            wa_domain_name=wa_domain_name,
            wa_additional_domain_names=wa_additional_domain_names,
            wa_bucket_policy_actions=wa_bucket_policy_actions,
            wa_bucket_props=wa_bucket_props,
            wa_cloud_front_distribution_default_behavior=wa_cloud_front_distribution_default_behavior,
            wa_default_root_object=wa_default_root_object,
            wa_enable_cloud_front_logging=wa_enable_cloud_front_logging,
            wa_error_response_page_path=wa_error_response_page_path,
            wa_origin_access_identity=wa_origin_access_identity,
            wa_path_to_content=wa_path_to_content,
            wa_sub_domain=wa_sub_domain,
        )

        return typing.cast(builtins.str, jsii.invoke(self, "getSiteDomain", [props]))

    @builtins.property
    @jsii.member(jsii_name="cdn")
    def cdn(self) -> _aws_cdk_aws_cloudfront_ceddda9d.Distribution:
        '''CloudFront distribution used in this construct.'''
        return typing.cast(_aws_cdk_aws_cloudfront_ceddda9d.Distribution, jsii.get(self, "cdn"))

    @builtins.property
    @jsii.member(jsii_name="cloudfrontOAI")
    def cloudfront_oai(self) -> _aws_cdk_aws_cloudfront_ceddda9d.OriginAccessIdentity:
        '''Origin Access Identity.'''
        return typing.cast(_aws_cdk_aws_cloudfront_ceddda9d.OriginAccessIdentity, jsii.get(self, "cloudfrontOAI"))

    @builtins.property
    @jsii.member(jsii_name="websiteBucket")
    def website_bucket(self) -> _wa_cdk_lite_597004ae.WaBucket:
        '''Bucket hosting website content.'''
        return typing.cast(_wa_cdk_lite_597004ae.WaBucket, jsii.get(self, "websiteBucket"))


__all__ = [
    "X8WebSiteProps",
    "X8Website",
]

publication.publish()

def _typecheckingstub__eef911c1fc2e9a12bd4f860fa566b7374a8ba5582d3a6a483773f671385807ec(
    *,
    wa_domain_name: builtins.str,
    wa_additional_domain_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    wa_bucket_policy_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    wa_bucket_props: typing.Optional[typing.Union[_wa_cdk_lite_597004ae.WaBucketProps, typing.Dict[builtins.str, typing.Any]]] = None,
    wa_cloud_front_distribution_default_behavior: typing.Optional[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.BehaviorOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    wa_default_root_object: typing.Optional[builtins.str] = None,
    wa_enable_cloud_front_logging: typing.Optional[builtins.bool] = None,
    wa_error_response_page_path: typing.Optional[builtins.str] = None,
    wa_origin_access_identity: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.OriginAccessIdentity] = None,
    wa_path_to_content: typing.Optional[builtins.str] = None,
    wa_sub_domain: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0fdea107373c62979d68a3dd6a36b3e12af38f9207c537b8977b8f035572f59(
    scope: _constructs_77d1e7e8.Construct,
    name: builtins.str,
    *,
    wa_domain_name: builtins.str,
    wa_additional_domain_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    wa_bucket_policy_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    wa_bucket_props: typing.Optional[typing.Union[_wa_cdk_lite_597004ae.WaBucketProps, typing.Dict[builtins.str, typing.Any]]] = None,
    wa_cloud_front_distribution_default_behavior: typing.Optional[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.BehaviorOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    wa_default_root_object: typing.Optional[builtins.str] = None,
    wa_enable_cloud_front_logging: typing.Optional[builtins.bool] = None,
    wa_error_response_page_path: typing.Optional[builtins.str] = None,
    wa_origin_access_identity: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.OriginAccessIdentity] = None,
    wa_path_to_content: typing.Optional[builtins.str] = None,
    wa_sub_domain: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c33cc3dfd199fa875209f2b95becc7fa167f83beb6362ad61fd5c9639d074b73(
    domain_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
