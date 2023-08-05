import requests
import sys
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from oblv.models.name_input import NameInput
from .api.account import get_user_accounts_account_get
from .api.auth import logout_session_logout_delete
from .api.deployment import (
    create_new_deployment_deployment_post,
    delete_deployment_deployment_delete,
    generate_build_args_deployment_arguments_get,
    get_available_deployments_deployment_available_get,
    get_deployment_info_deployment_get,
    get_deployment_roles_deployment_roles_get,
    get_supported_regions_deployment_supported_regions_get,
    get_user_owned_deployments_deployment_owned_get,
)
from .api.repo import (
    get_all_repos_repo_linked_get,
    get_repo_from_vcs_repo_get,
    get_repo_refs_repo_refs_get,
    get_repo_repo_repo_owner_repo_name_get,
    search_repo_from_vcs_repo_search_get,
)
from .api.service import (
    add_repo_service_repo_service_post,
    delete_repo_services_repo_service_delete,
    get_repo_service_yaml_form_content_repo_service_yaml_get,
    get_repo_services_repo_service_get,
    get_user_services_service_get,
    update_repo_service_repo_service_put,
    validate_repo_service_repo_service_validate_get,
)
from .api.user import (
    add_user_public_shared_key_user_psk_put,
    get_user_deployment_credit_usage_user_credit_usage_get,
    get_user_profile_view_user_profile_get,
    get_user_public_shared_key_user_psk_get,
    update_user_name_user_name_put,
    update_user_password_user_password_put,
)
from .client import AuthenticatedClient
from .config import URL
from .exceptions import BadYamlData
from .models import (
    PSK,
    CreateDeploymentInput,
    ServiceYamlAddInput,
    ServiceYamlUpdateInput,
    UserPasswordInput,
)
from .utils import bcolors


class OblvClient(AuthenticatedClient):
    def _method_wrapper(function):
        def wrap(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except Exception as e:
                reason = e.__str__()
                print(
                bcolors.RED
                + bcolors.BOLD
                + "Exception"
                + bcolors.BLACK
                + bcolors.ENDC
                + f": {e}",
                file=sys.stderr,
            )
                raise Exception(reason)

        return wrap

    @_method_wrapper
    def logout(self):
        """Logout Session

         This API invalidates the user's token. After a successul response, the user will not be able to use
        the auth token provided in the auth APIs.

        Returns:
            Response[Union[Any, HTTPValidationError, MessageModel]]
        """
        try:
            logout_session_logout_delete.sync(
                client=self, oblivious_user_id=self.oblivious_user_id
            )
        except Exception as e:
            raise e
        finally:
            self.token = ""
            self.oblivious_user_id = ""

    ###### Account Method ######

    @_method_wrapper
    def accounts(self):
        """Get User Accounts
         API to fetch user's linked VCS accounts
        Returns:
            Response[Union[Any, HTTPValidationError, List[Account], MessageModel]]
        """
        return get_user_accounts_account_get.sync(
            client=self, oblivious_user_id=self.oblivious_user_id
        )

    ############################

    ####### User Methods #######
    @_method_wrapper
    def psk(self):
        """Get User PSK
         API to fetch user's psk
        Returns:
            Response[Union[Any, HTTPValidationError, MessageModel, str]]
        """
        return get_user_public_shared_key_user_psk_get.sync(
            client=self,
            oblivious_user_id=self.oblivious_user_id,
            user_id=self.oblivious_user_id,
        )

    @_method_wrapper
    def credit_usage(self):
        """Get User Credit Usage
         API to fetch user's credit usage
        Returns:
            Response[Union[Any, HTTPValidationError, MessageModel, UserCreditUtilization]]
        """
        return get_user_deployment_credit_usage_user_credit_usage_get.sync(
            client=self, oblivious_user_id=self.oblivious_user_id
        )

    @_method_wrapper
    def set_psk(self, public_key):
        """Update user's publically shareable key
        API to update user's publically shareable key
        Args:
            public_key (str): Public Key to be shared
        Returns:
            Response[Union[None, HTTPValidationError, MessageModel]]
            None is returned if successful
        """

        input = PSK(public_key)
        return add_user_public_shared_key_user_psk_put.sync(
            client=self, oblivious_user_id=self.oblivious_user_id, json_body=input
        )

    @_method_wrapper
    def update_name(self, name):
        """Update Name
        API to update the name.
        Args:
            name (str): User Name
        Returns:
            Response[Union[Any, HTTPValidationError, MessageModel]]
        """
        update_user_name_user_name_put.sync(
            client=self,
            oblivious_user_id=self.oblivious_user_id,
            json_body=NameInput(name),
        )
        print("Name updated successfully")

    @_method_wrapper
    def update_password(self, old_pass, new_pass):
        """Update User's Password
         API to update user's password
        Args:
            old_pass (str): Old Password
            new_pass (str): New Password
        Returns:
            Response[Union[None, HTTPValidationError, MessageModel]]
                None is returned if successful
        """
        input = UserPasswordInput(old_password=old_pass, password=new_pass)
        update_user_password_user_password_put.sync(
            client=self, oblivious_user_id=self.oblivious_user_id, json_body=input
        )
        print("Password updated successfully")

    @_method_wrapper
    def user_profile(self):
        """Get User Profile
         API to fetch user's profile details
        Returns:
            Response[Union[Any, HTTPValidationError, MessageModel, UserProfileResponse]]
        """
        return get_user_profile_view_user_profile_get.sync(
            client=self, oblivious_user_id=self.oblivious_user_id
        )

    ############################

    ####### Repo Methods #######
    @_method_wrapper
    def get_repo(self, owner, name):
        """Get User Repo
         API to fetch user's repo information
        Args:
            owner (str): Repo Owner
            name (str): Repo Name
        Returns:
            Response[Union[Any, HTTPValidationError, MessageModel, Repo]]
        """
        return get_repo_repo_repo_owner_repo_name_get.sync(
            client=self,
            oblivious_user_id=self.oblivious_user_id,
            repo_owner=owner,
            repo_name=name,
        )

    @_method_wrapper
    def search_repo(self, keyword):
        """Add Repo Service With Yaml
         API to search a repository in VCS, on which the user has access (via their own account, or by any
        organization they are member of).
        Args:
            keyword (str): Search Keyword
        Returns:
            Response[Union[Any, HTTPValidationError, List[Repo], MessageModel]]
        """
        return search_repo_from_vcs_repo_search_get.sync(
            client=self, oblivious_user_id=self.oblivious_user_id, search_string=keyword
        )

    @_method_wrapper
    def linked_repos(self):
        """Get User Repos
         API to fetch user's repo without services
        Returns:
            Response[Union[Any, HTTPValidationError, List[RepoAllResponse], MessageModel]]
        """
        return get_all_repos_repo_linked_get.sync(
            client=self, oblivious_user_id=self.oblivious_user_id
        )

    @_method_wrapper
    def repo_refs(self, owner, name):
        """Get Repo Refs
         API to fetch the repository refs (branches and tags).
        Args:
            owner (str): Repo Owner
            name (str): Repo Name
        Returns:
            Response[Union[Any, HTTPValidationError, MessageModel, RefResponse]]
        """
        return get_repo_refs_repo_refs_get.sync(
            client=self,
            oblivious_user_id=self.oblivious_user_id,
            repo_owner=owner,
            repo_name=name,
        )

    @_method_wrapper
    def repos(self, page: int = 1, per_page: int = 10):
        """Get Repos From VCS
         API to get all the repositories from VCS, on which the user has access (via their own account, or by
        any organization they are member of).
        Args:
            page (int):  Page (Default 1)
            per_page (int):  Repositiories Per Page (Default 10)
        Returns:
            Response[Union[Any, HTTPValidationError, VCSRepoResponse]]
        """
        return get_repo_from_vcs_repo_get.sync(
            client=self,
            oblivious_user_id=self.oblivious_user_id,
            page=page,
            per_page=per_page,
        )

    ############################

    ##### Services Methods #####
    @_method_wrapper
    def add_service(
        self,
        repo_owner: str,
        repo_name: str,
        ref: str,
        ref_type: str = "branch",
        data: dict = {},
    ):
        """Add Repo Service
         API to create a service after validation.
        Args:
            repo_owner (str): Repo's Owner Name
            repo_name (str): Repo Name
            ref (str): Service Ref
            ref_type (Union[Unset, None, str]):  Ref Type branch/tag (Default 'branch')
            data (dict): Service Yaml Content in dictionary format. If provided, service.yaml file will be created/updated based on its existence.
        Returns:
            Response[Union[Any, HTTPValidationError, MessageModel, ServiceValidationResponse]]
        """
        if data != {}:
            try:
                req = requests.get(URL + "/service_schema")
                if req.status_code != 200:
                    raise Exception("Failed to validate service yaml data")
                validate(data, req.json())
            except ValidationError as e:
                raise BadYamlData(e.message)
            except Exception as e:
                raise e
        input = ServiceYamlAddInput.from_dict(data)
        return add_repo_service_repo_service_post.sync(
            client=self,
            oblivious_user_id=self.oblivious_user_id,
            ref=ref,
            ref_type=ref_type,
            repo_owner=repo_owner,
            repo_name=repo_name,
            json_body=input,
        )

    @_method_wrapper
    def remove_service(
        self, repo_owner: str, repo_name: str, ref: str, ref_type: str = "branch"
    ):
        """Delete Repo Service
         API to delete a service. It does not delete the existing deployments created from this service.
        Args:
            repo_owner (str): Repo's Owner Name
            repo_name (str): Repo Name
            ref (str): Service Ref
            ref_type (Union[Unset, None, str]):  Ref Type branch/tag (Default 'branch')
        Returns:
            Response[Union[Any, HTTPValidationError, MessageModel]]
        """
        delete_repo_services_repo_service_delete.sync(
            client=self,
            oblivious_user_id=self.oblivious_user_id,
            ref=ref,
            ref_type=ref_type,
            repo_name=repo_name,
            repo_owner=repo_owner,
        )
        print("Successfully removed service")

    @_method_wrapper
    def service_content(
        self, repo_owner: str, repo_name: str, ref: str, ref_type: str = "branch"
    ):
        """Get Repo Service Yaml
         API to fetch the service.yaml content as object for the given service.
        Args:
            repo_id (Union[Unset, str]): Repo Id
            ref (str): Service Ref
            ref_type (Union[Unset, None, str]):  Ref Type branch/tag (Default 'branch')
        Returns:
            Response[Union[Any, HTTPValidationError, MessageModel, ServiceContentResponse]]
        """
        return get_repo_service_yaml_form_content_repo_service_yaml_get.sync(
            client=self,
            oblivious_user_id=self.oblivious_user_id,
            repo_owner=repo_owner,
            repo_name=repo_name,
            ref=ref,
            ref_type=ref_type,
        )

    @_method_wrapper
    def repo_services(
        self,
        repo_owner: str,
        repo_name: str,
        page: int = 1,
        per_page: int = 10,
        get_all: bool = False,
    ):
        """Get Repo Services
         API to fetch all the services available for the given repository. This API is valid only for linked
        repositories.
        Args:
            repo_id (str): Repo Id
        Returns:
            Response[Union[Any, HTTPValidationError, List[ValidatedService], MessageModel]]
        """
        return get_repo_services_repo_service_get.sync(
            client=self,
            oblivious_user_id=self.oblivious_user_id,
            repo_owner=repo_owner,
            repo_name=repo_name,
            page=page,
            per_page=per_page,
            get_all=get_all,
        )

    @_method_wrapper
    def user_services(
        self,
        page: int = 1,
        per_page: int = 10,
        get_all: bool = False,
        search_keyword: str = "",
    ):
        """Get User Services
         API to fetch user's services
        Args:
            page (int):  Page (Default 1)
            per_page (str): services per page (Default 10)
            search_keyword (str): Search Keyword and is applied on repo full name (Default "")
            get_all (bool): To fetch all services at once (Default False)

        Returns:
            Response[Union[Any, HTTPValidationError, List[UserServices], MessageModel]]
        """
        return get_user_services_service_get.sync(
            client=self,
            oblivious_user_id=self.oblivious_user_id,
            page=page,
            per_page=per_page,
            get_all=get_all,
            search_term=search_keyword,
        )

    @_method_wrapper
    def update_service(
        self,
        repo_owner: str,
        repo_name: str,
        ref,
        ref_type: str = "branch",
        data: dict = {},
    ):
        """Update Repo Service With Yaml
         API to update a service, along with updating the service.yaml file. After updating the service.yaml file, the service is validate as well (for missing Dockerfile).
        Args:
            repo_owner (str): Repo's Owner Name
            repo_name (str): Repo Name
            ref (str): Service Ref
            ref_type (Union[Unset, None, str]):  Ref Type branch/tag (Default 'branch')
            data (dict): Service Yaml Content in dictionary format. If provided, service.yaml file will be created/updated based on its existence.

        Returns:
            Response[Union[Any, HTTPValidationError, MessageModel, ServiceValidationResponse]]
        """
        if data != {}:
            try:
                req = requests.get(URL + "/service_schema")
                if req.status_code != 200:
                    raise Exception("Failed to validate service yaml data")
                validate(data, req.json())
            except ValidationError as e:
                raise BadYamlData(e.message)
            except Exception as e:
                raise e
        input = ServiceYamlUpdateInput.from_dict(data)
        return update_repo_service_repo_service_put.sync(
            client=self,
            oblivious_user_id=self.oblivious_user_id,
            ref=ref,
            ref_type=ref_type,
            repo_owner=repo_owner,
            repo_name=repo_name,
            json_body=input,
        )

    @_method_wrapper
    def revalidate_service(
        self, repo_owner: str, repo_name: str, ref: str, ref_type: str = "branch"
    ):
        """Validate Repo Service
         API to validate a service with supported service schema. The checks include
        - Presence of service.yaml in ./oblivious folder.
        - Presence of Dockerfile in ./oblivious folder.
        - Content of service.yaml must be valid with respect to supported service schema.
        Args:
            repo_owner (str): Repo's Owner Name
            repo_name (str): Repo Name
            ref (str): Service Ref
            ref_type (Union[Unset, None, str]):  Ref Type branch/tag (Default 'branch')
        Returns:
            Response[Union[Any, HTTPValidationError, MessageModel, ServiceValidationResponse]]
        """
        return validate_repo_service_repo_service_validate_get.sync(
            client=self,
            oblivious_user_id=self.oblivious_user_id,
            repo_owner=repo_owner,
            repo_name=repo_name,
            ref=ref,
            ref_type=ref_type,
        )

    ############################

    #### Deployment Methods ####

    @_method_wrapper
    def deployment_info(self, deployment_id):
        """Get Deployment
         API to fetch a deployment's details.
        Args:
            deployment_id (str): Deployment Id
        Returns:
            Response[Union[Any, DeploymentResponse, HTTPValidationError, MessageModel]]
        """
        return get_deployment_info_deployment_get.sync(
            client=self,
            oblivious_user_id=self.oblivious_user_id,
            deployment_id=deployment_id,
        )

    @_method_wrapper
    def create_deployment(self, deployment: CreateDeploymentInput):
        """Create Deployment
         API to create a new deployment.
        Args:
            deployment (CreateDeploymentInput): Deployment Details Input
        Returns:
            Response[Union[Any, CreateDeploymentResponse, HTTPValidationError, MessageModel]]
        """
        return create_new_deployment_deployment_post.sync(
            client=self, oblivious_user_id=self.oblivious_user_id, json_body=deployment
        )

    @_method_wrapper
    def remove_deployment(self, deployment_id):
        """Delete Deployment
         API to initiate termination of a deployment.
        Args:
            deployment_id (str): Deployment Id
        Returns:
            Response[Union[Any, HTTPValidationError, MessageModel]]
        """
        return delete_deployment_deployment_delete.sync(
            client=self,
            oblivious_user_id=self.oblivious_user_id,
            deployment_id=deployment_id,
        )

    @_method_wrapper
    def generate_deployment_build_args(
        self, owner: str, repo: str, ref: str, ref_type: str = "branch"
    ):
        """Get Build Deployment Arguments
        API to fetch the arguments schema necessary for creating a deployment. It also gives the commit sha,
        at which point it was generated. This is to be passed to the create deployment API.
        Note - A service could have different build args schema depending on the service's commit history.
        Args:
            owner (str): Repo Owner
            repo (str): Repo Name
            ref (str): Service Ref
            ref_type (str): Ref Type branch/tag (Default 'branch')
        Returns:
            Response[Union[Any, BuildArgsSchema, HTTPValidationError, MessageModel]]
        """
        return generate_build_args_deployment_arguments_get.sync(
            client=self,
            oblivious_user_id=self.oblivious_user_id,
            repo=repo,
            owner=owner,
            ref=ref,
        )

    @_method_wrapper
    def available_deployments(self):
        """Get Available Deployments
         API to fetch all the deployments the user can connect to.
        Returns:
            Response[Union[Any, HTTPValidationError, List[DeploymentComplete], MessageModel]]
        """
        return get_available_deployments_deployment_available_get.sync(
            client=self, oblivious_user_id=self.oblivious_user_id
        )

    @_method_wrapper
    def deployment_roles(self, deployment_id):
        """Get Deployment Roles
         API to get a deployment's roles.
        Args:
            deployment_id (str): Deployment Id
        Returns:
            Response[Union[Any, HTTPValidationError, List[RoleResponse], MessageModel]]
        """
        return get_deployment_roles_deployment_roles_get.sync(
            client=self,
            oblivious_user_id=self.oblivious_user_id,
            deployment_id=deployment_id,
        )

    @_method_wrapper
    def supported_aws_regions(self):
        """Deployment Supported Regions
         API to fetch a deployment's details.
        Returns:
            Response[Union[Any, MessageModel]]
        """
        return get_supported_regions_deployment_supported_regions_get.sync(client=self)

    @_method_wrapper
    def deployments(self):
        """Get Owned Deployments
         API to fetch a user's owned deployments.
        Returns:
            Response[Union[Any, HTTPValidationError, List[DeploymentResponse], MessageModel]]
        """
        return get_user_owned_deployments_deployment_owned_get.sync(
            client=self, oblivious_user_id=self.oblivious_user_id
        )

    ############################
