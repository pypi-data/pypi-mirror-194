"""
Use the `AdminConfig` object to invoke configuration commands and to create or 
change elements of the WebSphere® Application Server configuration, for example, 
creating a data source.

For more info see the [official documentation](https://www.ibm.com/docs/en/was-nd/8.5.5?topic=scripting-commands-adminconfig-object-using-wsadmin).
"""
from typing import Any, Literal, Optional, Union, overload

from .typing_objects.object_name import ConfigurationContainmentPath, ConfigurationObjectName, RunningObjectName
from .typing_objects.wsadmin_types import MultilineList, MultilineTableWithHeader, MultilineTableWithoutHeader, OpaqueDigestObject
from .typing_objects.object_types import ObjectType

def attributes(object_type: ObjectType, /) -> MultilineTableWithoutHeader[str]:
    """Get a multiline string containing the top level attributes for the given type.

    Args:
        object_type (ObjectType): name of the object type. Use [`AdminConfig.types()`][wsadmin_type_hints.AdminConfig.types] to get a list of available types.

    Returns:
        attributes_table (MultilineTableWithoutHeader[str]): Multiline table with the attributes of the given type.
            The first "word" in each line is the **attribute name**, and the rest is the **attribute** value **type**.
    
    Example:
        ```pycon
        >>> print(AdminConfig.attributes("Server"))
        adjustPort Boolean
        changeGroupAfterStartup String
        changeUserAfterStartup String
        clusterName String
        [...]
        ```
    """
    ...

# TODO: Check return type
def checkin(document_uri: str, file_name: str, opaque_object: OpaqueDigestObject, /) -> Any:
    """Checks a file that the document URI describes into the configuration repository.
    This method only applies to deployment manager configurations.

    Args:
        document_uri (str): The document URI, relative to the root of the configuration repository.
        file_name (str): The name of the source file to check.
        opaque_object (OpaqueDigestObject): The object returned by a prior call to the `AdminConfig.extract()` command.
    
    Question: More testing needed
        The **return type** needs to be checked.
    """
    ...

def convertToCluster(): # undocumented
    ...

def create(): # undocumented
    ...

def createClusterMember(): # undocumented
    ...

def createDocument(): # undocumented
    ...

def createUsingTemplate(): # undocumented
    ...

def defaults(object_type: ObjectType) -> MultilineTableWithHeader[str]:
    """ Displays all the possible attributes contained by an object of type `object_type`, along with 
        the type and default value of each attribute, if the attribute has a default value.

    Args:
        object_type (ObjectType): The type of the object

    Returns:
        defaults (MultilineTableWithHeader[str]): Tab-separated table with all the attribute defaults. 
            The table consists of the following columns:
            
            1. `Attribute`: Attribute name
            2. `Type`: Attribute type
            3. `Default`: Default value


    Example:
        ```pycon
        >>> print AdminConfig.defaults("Server")
        Attribute                       Type                            Default
        name                            String
        clusterName                     String
        modelId                         String
        shortName                       String
        uniqueId                        String
        developmentMode                 boolean                         false
        parallelStartEnabled            boolean                         true
        [...]
        ```
    """
    ...

def deleteDocument(): # undocumented
    ...

def existsDocument(): # undocumented
    ...

def extract(document_uri: str, filename: str, /) -> OpaqueDigestObject:
    """Extracts a configuration repository file that is described by the document URI and places it in the file named by filename. 
    This method only applies to deployment manager configurations.

    Args:
        document_uri (str): The document URI, relative to the root of the configuration repository. This MUST exist in the repository.
        filename (str): The name of the source file to check. If it exists already, it will be overwritten.

    Returns:
        OpaqueDigestObject: An opaque "digest" object which should be used to check the file back in using the checkin command.
    """
    ...

def getCrossDocumentValidationEnabled(): # undocumented
    ...

def getid(containment_path: ConfigurationContainmentPath) -> ConfigurationObjectName:
    """Returns the unique configuration ID for an object described by the
        given containment path.

    Args:
        containment_path (ConfigurationContainmentPath): The containment path of the requested object

    Returns:
        configuration_id (ConfigurationObjectName): The configuration ID for the object

    Example:
        ```pycon
        >>> print(AdminConfig.getid("/Node:myNode/Server:myServer/"))
        myServer(cells/myCell/nodes/myNode/servers/myServer|server.xml#Server_1)
        ```
    """
    ...

def getObjectName(configuration_id: ConfigurationObjectName) -> Union[RunningObjectName, Literal[""]]:
    """ Returns a string version of the ObjectName for the MBean that corresponds to this configuration ID. 
    
    If there is no such running MBean this returns an empty string.

    Args:
        configuration_id (ConfigurationObjectName): The configuration ID of the object

    Returns:
        mbean_object_name (RunningObjectName | Literal[""]): ObjectName of the MBean corresponding to the specified configuration ID.

    Example:
        ```pycon
        # Search the configuration ID of the object
        >>> server = AdminConfig.getid("/Node:myNode/Server:myServer/")
        >>> print(server)
        myServer(cells/myCell/nodes/myNode/servers/myServer|server.xml#Server_1)

        # Retrieve the running object from the configuration ID (not running if empty string)
        >>> server_instance = AdminConfig.getObjectName(server)
        >>> print(server_instance)
        WebSphere:name=myServer,process=myServer,platform=proxy,node=myNode,j2eeType=J2EEServer,version=9.0.5.14,type=Server,mbeanIdentifier=cells/myCell/nodes/myNode/servers/myServer/server.xml#Server_1,cell=myCell,spec=1.0,processType=ManagedProcess
        ```
    """    
    ...

def getObjectType(): # undocumented
    ...

def getSaveMode(): # undocumented
    ...

def getValidationLevel(): # undocumented
    ...

def getValidationSeverityResult(): # undocumented
    ...

def hasChanges() -> bool:
    """ Check if there are unsaved configuration changes.

    Returns:
        has_changes (bool): Truthy (actual value is `1`) if unsaved configuration changes exist, falsy (`0`) otherwise.
    
    Example:
        ```pycon
        >>> print(AdminConfig.hasChanges())
        0
        ```
    """
    ...

# --------------------------------------------------------------------------
@overload
def help() -> str:
    """ Displays general help for the `AdminConfig` module.

    Returns:
        help (str): A general help.
    """
    ...

@overload
def help(method_name: str) -> str:
    """ Displays help for the `AdminConfig` method specified by `method_name`.

    Args:
        method_name (str): The name of the method whose description needs to be retrieved.

    Returns:
        help (str): A more specific help regarding the method `method_name`.
    """
    ...


def help(method_name: str = "") -> str: # type: ignore[misc]
    """ Displays help for the `AdminConfig` module and its methods.

    Args:
        method_name (str, optional): The name of the method whose description needs to be retrieved.

    Returns:
        message (str): The help message regarding the method `method_name` (if provided), otherwise the description of the `AdminConfig` module and its methods.
    
    Example:
        - To get an **overview** of the module and its methods:
        ```pycon
        >>> print(AdminConfig.help())
        WASX7053I: The AdminConfig object communicates with the
        Config Service in a WebSphere server to manipulate configuration data
        for a WebSphere installation.  AdminConfig has commands to list, create,
        remove, display, and modify configuration data, as well as commands to
        display information about configuration data types.
        [...]
        ```

        - For a more detailed description of a **single method**:
        ```pycon
        >>> print(AdminConfig.help("attributes"))
        WASX7061I: Method: attributes

        Arguments: type

        Description: Displays all the possible attributes contained by an
        object of type "type."  The attribute types are also displayed; when
        the attribute represents a reference to another object, the type of
        [...]
        ```
    """
    ...
# --------------------------------------------------------------------------

def installResourceAdapter(): # undocumented
    ...

# --------------------------------------------------------------------------
@overload
def list(object_type: ObjectType, /) -> MultilineList[ConfigurationObjectName]:
    """Lists all the configuration objects of the type named by `object_type`.

    Args:
        object_type (ObjectType): The name of the object type.

    Returns:
        objects(MultilineList[ConfigurationObjectName]): Multiline list of objects of the given type.
    """
    ...

@overload
def list(object_type: ObjectType, scope: ConfigurationObjectName, /) -> MultilineList[ConfigurationObjectName]:
    """Lists all the configuration objects of the type named by `object_type` in the scope of `scope`.

    Args:
        object_type (ObjectType): The name of the object type.
        scope (ConfigurationObjectName): The scope of the search.

    Returns:
        objects(MultilineList[ConfigurationObjectName]): Multiline list of objects of the given type found under the scope of `scope`.
    """
    ...

@overload
def list(object_type: ObjectType, pattern: str, /) -> MultilineList[ConfigurationObjectName]:
    """Lists all the configuration objects of the type named by `object_type` and matching 
    wildcard characters or Java regular expressions.

    Args:
        object_type (ObjectType): The name of the object type.
        pattern (str): The pattern (wildcard characters or Java regular expressions) that needs to be matched.

    Returns:
        objects(MultilineList[ConfigurationObjectName]): Multiline list of objects of the given type matching the pattern `pattern`
    """
    ...

def list(object_type: ObjectType, scope_or_pattern: Optional[Union[ConfigurationObjectName, str]] = "", /) -> MultilineList[ConfigurationObjectName]: # type: ignore[misc]
    """Lists all the configuration objects of the type named by `object_type`.
    
    Args:
        object_type (ObjectType): The name of the object type.
        scope_or_pattern (Union[ConfigurationObjectName, str], optional): This parameter causes a different behaviour depending on its type:
            
            - `ConfigurationObjectName`: Limit the search within the scope of the configuration object named by `scope`.
            - `str`: Search all the configuration objects matching wildcard characters or Java regular expressions.

    Returns:
        objects(MultilineList[ConfigurationObjectName]): Multiline list of objects of a given type, possibly scoped by a parent.
    
    Example:
        If the `scope_or_pattern` parameter is omitted, then will be returned a list of all servers defined:
        ```pycon
        >>> print(AdminConfig.list("Server"))
        ```

        You can narrow the search using the `scope_or_pattern` parameter:

        - Limit the search to only the servers under the **scope** of the node `node`:
            ```pycon
            >>> node = AdminConfig.list("Node").splitlines()[0]
            >>> print(AdminConfig.list("Server", node))
            ```
        - Search the servers matching a specific **wildcard** pattern:
            ```pycon
            >>> print(AdminConfig.list("Server", "server1*"))
            ```
        - Search the servers matching a specific **regular expression** pattern:
            ```pycon
            >>> print(AdminConfig.list("Server", "server1.*"))
            ```
    """
    ...
# --------------------------------------------------------------------------

def listTemplates(): # undocumented
    ...

def modify(): # undocumented
    ...

def parents(): # undocumented
    ...

def queryChanges() -> MultilineList[str]:
    """Returns a list of unsaved configuration files.

    Returns:
        changed_files (str): Multiline list of unsaved configuration files.

    Example:
        - If some unsaved changes are **found**:
        ```pycon
        >>> print(AdminConfig.queryChanges())
        WASX7146I: The following configuration files contain unsaved changes:
        cells/mycell/nodes/mynode/servers/server1|resources.xml
        ```
        
        - In case unsaved changes are **not found**:
        ```pycon
        >>> print(AdminConfig.queryChanges())
        WASX7241I: There are no unsaved changes in this workspace.
        ```

    !!! Warning
        **Do NOT** use this method as a way to **check** if there are changes that need to be saved!
        If that is your goal, see if you can use the [**`AdminConfig.hasChanges()`**][wsadmin_type_hints.AdminConfig.hasChanges] method instead.

        Use the `AdminConfig.queryChanges()` method ONLY to **show** which files have been changed but not saved.
    """
    ...

def remove(): # undocumented
    ...

def required(object_type: ObjectType) -> MultilineTableWithHeader[str]:
    """Displays a table with the required attributes contained by an object of type `object_type`.

    Args:
        object_type (ObjectType): The object type as returned by the [`AdminConfig.types()`][wsadmin_type_hints.AdminConfig.types] method.

    Returns:
        required_schema (MultilineTableWithHeader[str]): A table with the required attributes contained by the object. 
            The first row contains the header.
    
    Example:
        This is an example of how to use the `required()` method:
        ```pycon
        >>> print(AdminConfig.required("Server"))
        Attribute                       Type
        name                            String
        ```
    
    Warning:
        When the type has **no required attributes**, the returned table will NOT be an empty string.
        Instead, it will contain only the message _`WASX7361I`_:
        ```pycon
        >>> print(AdminConfig.required("JavaVirtualMachine"))
        WASX7361I: No required attribute found for type "JavaVirtualMachine".
        ```
        
    !!! abstract "See also"
        - For a list of all the available object types, see [`AdminConfig.types()`][wsadmin_type_hints.AdminConfig.types]
        - For a list of all the attributes available for the requested object type, see [`AdminConfig.attributes()`][wsadmin_type_hints.AdminConfig.attributes]
        - For a list of all the default values for the attributes of the requested object type, see [`AdminConfig.defaults()`][wsadmin_type_hints.AdminConfig.defaults]
    """
    ...

def reset() -> Literal['']:
    """ Discard unsaved configuration changes.
        
    Returns:
        empty (Literal['']): An empty string is always returned
    
    !!! abstract "See also"
        - For the opposite operation, see [`AdminConfig.save()`][wsadmin_type_hints.AdminConfig.save]
    """
    ...

def resetAttributes(): # undocumented
    ...

def save() -> Literal['']:
    """ Commits unsaved changes to the configuration repository.
    
    Returns:
        empty (Literal['']): An empty string is always returned

    !!! abstract "See also"
        - For the opposite operation, see [`AdminConfig.reset()`][wsadmin_type_hints.AdminConfig.reset]
    """
    ...

def setCrossDocumentValidationEnabled(): # undocumented
    ...

def setSaveMode(): # undocumented
    ...

def setValidationLevel(): # undocumented
    ...

def show(): # undocumented
    ...

def showall(): # undocumented
    ...

def showAttribute(configuration_id: ConfigurationObjectName, attribute: str, /) -> str:
    """Shows the value of the single attribute specified for the configuration object named by `configuration_id`.
    
    The output of this command is different from the output of [`AdminConfig.show()`][wsadmin_type_hints.AdminConfig.show] when a single
    attribute is specified: the `AdminConfig.showAttribute` command does not display a
    list containing the attribute name and value; rather, the **attribute value alone** is displayed.

    Args:
        configuration_id (ConfigurationObjectName): The configuration ID for the parent object of the `attribute`.
        attribute (str): The name of the attribute value to retrieve.

    Returns:
        attribute_value (str): The value of the single attribute specified.

    !!! Tip
        For a complete list of attributes available for the configuration object use the [`AdminConfig.attributes()`][wsadmin_type_hints.AdminConfig.attributes] 
        method passing the object type as a parameter.

        For example, if you don't remember the name of an attribute for the `Server` object type, you can `print(AdminConfig.attributes("Server"))`.
        
    Example:
        ```pycon
        >>> server = AdminConfig.getid("/Node:myNode/Server:myServer/")
        >>> server_name, server_cluster = AdminConfig.showAttribute(server, "name"), AdminConfig.showAttribute(server, "clusterName")
        >>> print("Server '%s' is part of cluster '%s'" % (server_name, server_cluster))
        Server 'myServer' is part of cluster 'myCluster'
        ```
    """
    ...

# --------------------------------------------------------------------------
@overload
def types() -> MultilineList[ObjectType]:
    """Displays all the possible top-level configuration object types.

    Returns:
        types(MultilineList[ObjectType]): All the top-level configuration object types.
    """
    ...

@overload
def types(pattern: str) -> MultilineList[ObjectType]:
    """Displays all the possible top-level configuration object types matching
    with the `pattern`, which can be a wildcard or a regular expression.

    Args:
        pattern (str): A wildcard or a regular expression matching the type to search.

    Returns:
        types(MultilineList[ObjectType]): A multiline list of all the possible top-level configuration object types
            matching the provided `pattern`.
    """
    ...

def types(pattern: Optional[str] = "") -> MultilineList[ObjectType]: # type: ignore[misc]
    """Displays all the possible top-level configuration object types, restricting the 
    search to the types matching the `pattern` parameter, if specified.

    Args:
        pattern (Optional[str], optional): A wildcard or a regular expression matching the type to search.
    
    Returns:
        types(MultilineList[ObjectType]): A multiline list of all the possible top-level configuration object types
            matching the provided `pattern` (if specified).

    Example:
        - Print **all** the available types:
            ```pycon
            >>> print(AdminConfig.types())
            AccessPointGroup
            Action
            ActivationSpec
            ActivationSpecTemplateProps
            ActiveAffinityType
            [...]
            ```
        - Print **only** the types matching the regex `No.*`:
            ```pycon
            >>> print(AdminConfig.types("No.*"))
            NoOpPolicy
            Node
            NodeAgent
            NodeGroup
            NodeGroupMember
            ```
    """
    ...
# --------------------------------------------------------------------------

def uninstallResourceAdapter(): # undocumented
    ...

def unsetAttributes(): # undocumented
    ...

def validate(): # undocumented
    ...
