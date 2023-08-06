import re
import requests
import simplejson as json
import time
import urllib
import urllib.parse
import validators

from .auth import HTTPGenericHeaderAuth, HTTPGenericParameterAuth
from .base import TinApiBase, TinApiClass
from .config import TinConfig
from .exceptions import TinInvalidArgs, TinError, TinObjectNotFound
from .models import TinApiModelFactory
from .response import TinApiResponseFactory

from deepmerge import always_merger


class TinApi(TinApiClass):
    """The TinApi class represents a complete REST API

    This represents a parent class which contains the object hierarchy which
    will represent the endpoints of the defined REST API.

    Args:
        **kwargs: Arbitrary keyword arguments which will be passed to TinConfig

    Attributes:
        conf (TinConfig): An TinConfig object representing the configuration for
            this API
        tokenre (sre): Compiled regex for locating tokens in the url path string
    """

    def __init__(self, config=None, **kwargs):
        super().__init__()

        if config is None:
            self.conf = TinConfig(**kwargs)
        else:
            if isinstance(config, TinConfig):
                self.conf = config
            else:
                raise TinInvalidArgs("Config must be a TinConfig instance")

        self.obj_path = self.conf.api_name

        self._headers = self.conf.headers
        self._auth_obj = self._default_auth()

        self._session = requests.Session() if self.conf.use_session else None

        self.tokenre = re.compile(":([a-zA-Z0-9_-]+)")

        self._model_factory = TinApiModelFactory()
        self._recurse_build_method_path(self, self.conf.apidata, self.obj_path)

    def _recurse_build_method_path(self, obj, api_data, obj_path=None):

        if obj_path is None:
            obj_path = self.conf.api_name

        for cls_name, cls_data in api_data.items():

            new_type = type(cls_name, (TinApiClass,), {})
            container_path = "{}.{}".format(obj_path, cls_name)
            setattr(new_type, "_obj_path", container_path)

            if cls_data.get("model"):

                model_data = self.conf.models.get(cls_data["model"], {})
                model_type = self._model_factory(cls_data["model"], model_data)
                setattr(new_type, "_model", model_type)
                setattr(
                    model_type,
                    "_obj_path",
                    "{}.{}".format(container_path, cls_data["model"]),
                )

            for attr in ["response_data_key", "objects_data_key", "singleton_data_key"]:
                if cls_data.get(attr):
                    setattr(
                        new_type,
                        attr,
                        cls_data.get(attr),
                    )

            new_obj = new_type()

            obj.add_class(cls_name, new_obj)

            if cls_data.get("methods"):
                # If a child node has 'methods', it's an endpoint

                crud_methods = ["create", "read", "update", "delete"]

                # For each defined method, add an TinApiMethod as
                # an attribute in the current TinApiClass instance
                for mth, mth_data in cls_data["methods"].items():

                    new_method = TinApiMethod(self, new_obj, mth, mth_data)
                    new_method.obj_path = "{}.{}".format(container_path, mth)

                    new_obj.add_method(mth, new_method)

                    # If there is an associated model, it will get ome of the same
                    # methods as the parent class
                    if hasattr(new_type, "_model") and new_type._model is not None:
                        if mth_data.get("model_method_add", None) is False:
                            continue

                        if (
                            mth_data.get("model_method_add", None) is True
                            or cls_data.get("model_methods_add_all", None) is True
                        ):
                            method_name = mth_data.get("model_method_name") or mth
                            new_obj.model.add_method(method_name, new_method)

                            if "crud_label" in mth_data:
                                crud_method = mth_data["crud_label"].lower()
                                if crud_method in crud_methods:
                                    new_obj.model.CRUD_METHODS[
                                        crud_method
                                    ] = new_obj.model.get_method(method_name)

                                    # There can be only one method assigned to each CRUD
                                    # action. As we assign them, remove them from the
                                    # list. If a second/duplicate label shows up in the
                                    # config, it'll just be ignored for not being in
                                    # crud_methods
                                    crud_methods.remove(crud_method)

            else:
                # If there are no methods, it's a container class
                self._recurse_build_method_path(new_obj, cls_data, container_path)

    @property
    def request(self):
        if self._session:
            return self._session
        return requests

    @property
    def headers(self):
        return self._headers

    def set_headers(self, headers, override=False):
        if override:
            self._headers = headers
        else:
            self._headers.update(headers)

    @property
    def auth(self):
        return self._auth_obj

    def set_auth(self, auth_obj):
        self._auth_obj = auth_obj

    def _default_auth(self):
        """Returns a requests auth instance based on the api config"""

        if self.conf.auth_type == "basic":
            return requests.auth.HTTPBasicAuth(
                self.conf.credentials.get("username", None),
                self.conf.credentials.get("password", None),
            )
        elif self.conf.auth_type == "header":
            return HTTPGenericHeaderAuth(self.conf.credentials)
        elif self.conf.auth_type == "param":
            return HTTPGenericParameterAuth(self.conf.credentials)
        else:
            return None


class TinApiMethod(TinApiBase):
    def __init__(self, apiobj, clsobj, name, method_data, obj_path=None):
        """
        The TinApiMethod represents an endpoint method to call on a remote REST API.

        Args:
            apiobj (TinApi): The parent object that contains all classes and methods
                of this API
            clsobj (TinApiClass): The parent object of this method
            name (str): The name of this method
            method_data (dict): A set of information about this method as defined in
                the config YAML

        Attributes:
            name (str): The method name
            api (TinApi): The toplevel APi object
            cls (TinApiClass): The immediate parent TinApiClass object
            method_data (dict): A set of k->v information about the method

        """
        self.name = name
        self.api = apiobj
        self.cls = clsobj
        self._method_data = method_data
        self._response_factory = TinApiResponseFactory()

        self.method = self._method_data["method"]
        self.crud_label = self._method_data.get("crud_label", None)
        self.singleton = self._method_data.get("singleton", False)
        self.response_data_key = self._method_data.get("response_data_key", None)
        self.objects_data_key = self._method_data.get("objects_data_key", None)
        self.singleton_data_key = self._method_data.get("singleton_data_key", None)

        if self._method_data.get("nobase", False):
            self.path = self._method_data["path"]
        else:
            self.path = "{}{}".format(self.api.conf.basepath, self._method_data["path"])

        if "scheme" in self._method_data:
            self._scheme = self._method_data["scheme"]
        else:
            self._scheme = self.api.conf.scheme

        if "host" in self._method_data:
            self._host = self._method_data["host"]
        else:
            self._host = self.api.conf.host

        if "port" in self._method_data:
            self._port = self._method_data["port"]
        else:
            self._port = self.api.conf.port

        # Merge headers for the method if any are set
        method_headers = dict(self.api.headers)
        self._headers = always_merger.merge(
            method_headers, self._method_data.get("headers", {})
        )

        # If the method specifies an expected return code, grab it, otherwise
        # default to 200
        if "expect" in self._method_data:
            if isinstance(self._method_data["expect"], list):
                self.expect_return_codes = [int(r) for r in self._method_data["expect"]]
            else:
                self.expect_return_codes = [self._method_data["expect"]]
        else:
            self.expect_return_codes = [200]

        if "paginate" in self._method_data:
            self._paginate = self._method_data["paginate"]
        else:
            self._paginate = True

        if "paginate_delay" in self._method_data:
            self._paginate_delay = self._method_data["paginate_delay"]
        else:
            self._paginate_delay = 0

        self.default_params = (
            dict(self.api.conf.default_params)
            if hasattr(self.api.conf, "default_params")
            else {}
        )

        self.default_tokens = (
            dict(self.api.conf.default_tokens)
            if hasattr(self.api.conf, "default_tokens")
            else {}
        )

        # If the method has additional default params, merge them in
        if "default_params" in self._method_data:
            self.default_params.update(self._method_data["default_params"])

        # If the method has additional default tokens, merge them in
        if "default_tokens" in self._method_data:
            self.default_tokens.update(self._method_data["default_tokens"])

        self.url = "%s://%s:%s%s" % (
            self._scheme,
            self._host,
            self._port,
            self.path,
        )

        super().__init__()

    @property
    def headers(self):
        return self._headers

    def to_json(self):

        return json.dumps(
            {
                "scheme": self._scheme,
                "host": self._host,
                "port": self._port,
                "credentials": self.api.conf.credentials,
                "url": self.url,
                "method_data": self._method_data,
            }
        )

    def path_tokens(self):
        return self.api.tokenre.findall(self.path)

    def __call__(self, id=None, **kwargs):

        # This is where we can put validations on the kwargs,
        # based off data in api.yml (not there yet)

        url = self.url  # FIXME: what?
        data = {}
        params = dict(self.default_params)
        tokens = dict(self.default_tokens)

        # if this is true, TinApiResponseFactory will not instantiate model instances
        # from response data, and just return JSON.  Default is False.
        nomodel = kwargs.pop("nomodel") if "nomodel" in kwargs else False

        # Overwrite with provided arguments. Pop the value out of kwargs.
        if "params" in kwargs:
            params.update(kwargs.pop("params"))

        # allow header overrides
        call_headers = dict(self._headers)
        call_headers = always_merger.merge(call_headers, kwargs.pop("headers", {}))

        # lower header keys to make their names predictable so we can inspect them later
        call_headers = {k.lower(): v for k, v in call_headers.items()}

        # No defaults for data.
        if "data" in kwargs:
            data = kwargs.pop("data")
        else:
            data = None

        # Support overriding default paginate behavior with a kwarg
        if "paginate" in kwargs:
            paginate = kwargs.pop("paginate")
        else:
            paginate = self._paginate

        # Support overriding default paginate_delay behavior with a kwarg
        if "paginate_delay" in kwargs:
            paginate_delay = kwargs.pop("paginate_delay")
        else:
            paginate_delay = self._paginate_delay

        # If 'id' is passed as a positional, it overrides 'id' as a kwarg
        if id is not None:
            kwargs["id"] = id

        # The remaining kwargs *should* correspond to path tokens
        # Merge with defaults, if they exist
        tokens.update(kwargs)

        # Ensure all our path tokens are accounted for
        for tok in self.path_tokens():
            if tok not in tokens:
                raise TinInvalidArgs(
                    "%s called with missing token "
                    "argument %s. For path %s" % (self, tok, self.path)
                )

        # Presence of our path tokens is verified. Replace them in our url
        for k, v in tokens.items():
            url = url.replace(":%s" % k, str(v))

        try:
            response_data = None
            next_params = None

            while True:

                # Grab the requests method based on http method name
                try:
                    requests_method = getattr(self.api.request, self.method.lower())
                except AttributeError:
                    raise TinError("Invalid HTTP method: {}".format(self.method))

                # If we have parameters from a loop which overlap with our original params
                # merge them over top of the original params
                if next_params:
                    params = always_merger.merge(params, next_params)

                # Common arguments with all methods
                request_args = {
                    "headers": call_headers,
                    "auth": self.api.auth,
                    "verify": self.api.conf.ssl["verify"],
                    "params": urllib.parse.urlencode(
                        params, quote_via=urllib.parse.quote
                    ),
                }
                if self.api.conf.ssl.get("cert", None):
                    request_args["cert"] = self.api.conf.ssl["cert"]

                # Add data if we have any
                if data:
                    if call_headers.get("content-type") == "application/json":
                        request_args["data"] = json.dumps(data)
                    else:
                        request_args["data"] = data

                # Call the requests method
                attempt = 1
                while attempt < self.api.conf.ratelimit_max_retry:
                    response = requests_method(url, **request_args)
                    if response.status_code == 429:
                        time.sleep(self.api.conf.ratelimit_pause)
                        attempt += 1
                    else:
                        break
                else:
                    raise TinError(
                        f"Rate limited and max retry of {self.api.conf.ratelimit_max_retry} reached"
                    )

                if response.status_code == 404:
                    raise TinObjectNotFound(
                        "Object not found. Tried: {}. "
                        "Remote API says: {}".format(url, response.text)
                    )
                elif response.status_code not in self.expect_return_codes:
                    raise TinError(
                        "ERROR at {} Got return code {}, expected {}. "
                        "Remote API says: {}".format(
                            url,
                            response.status_code,
                            ",".join([str(r) for r in self.expect_return_codes]),
                            response.text,
                        )
                    )

                if response.status_code == 204:
                    response_data = None
                    break
                elif response.text:
                    try:
                        current_response_data = response.json()
                    except Exception:
                        # FIXME: excessively generic exception
                        raise TinError(
                            "ERROR decoding response JSON. "
                            "Raw response is: {}".format(response.content)
                        )

                    # If we're paginating, this recursively merges the current response
                    # with preceding ones
                    if response_data:
                        response_data = always_merger.merge(
                            response_data, current_response_data
                        )
                    else:
                        response_data = current_response_data

                    if "next" in response.links:
                        next_url = response.links["next"].get("url", "")

                        if validators.url(next_url) and paginate:
                            if "?" in next_url:
                                url, query_string = next_url.split("?")
                                next_params = dict(urllib.parse.parse_qsl(query_string))
                            else:
                                url = next_url
                            time.sleep(paginate_delay)
                        else:
                            break
                    else:
                        break
                else:
                    break

                # This next bit appears to have been almost exclusively for Oomnitza and
                # their weird header-based paginating.  I'll leave it here for reference
                # if we find enough APIs that do something like this but otherwise I
                # think this would be better in the code using Tin.

                # # Handle pagination types
                # # "header_count" expects a total passed over in the HTTP header
                # if (hasattr(self.api.conf, "pagination")) and (
                #     self.api.conf.pagination["type"] == "header_count"
                # ):
                #     header_count = response.headers.get(
                #         self.api.conf.pagination["header"], "0"
                #     )  # if the specified header doesn't exist, assume 0 addt'l pages
                #
                #     response_count["current"] = len(current_response_data)
                #     response_count["total"] = len(response_data)
                #
                #     # If we haven't fetched all the records, set the config'd
                #     # path or params then continue
                #     if response_count["total"] < int(header_count):
                #
                #         v = self.api.conf.pagination["value"]
                #
                #         if "param" in self.api.conf.pagination:
                #             p = self.api.conf.pagination["param"]
                #             params[p] = response_count[v]
                #         elif "path" in self.api.conf.pagination:
                #             n = self.api.conf.pagination["path"]
                #             path = n % response_count[v]
                #             url = "%s/%s" % (url, path)
                #     else:
                #         break

        except requests.exceptions.HTTPError as e:
            raise TinError("ERROR: %s" % e)

        return self._response_factory(response_data, response, self, nomodel)
