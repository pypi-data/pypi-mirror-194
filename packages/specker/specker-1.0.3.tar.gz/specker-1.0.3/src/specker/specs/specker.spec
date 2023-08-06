{
    "required": {
        "required": false,
        "default": false,
        "type": "bool",
        "comment": "Whether or not this Option is required"
    },
    "default": {
        "required": false,
        "type": "any",
        "comment": "Default Value if not required and not set"
    },
    "type": {
        "required": true,
        "default": "any",
        "type": "str",
        "comment": "Type the Value must be. Must be one of: int, str, list, dict, bool, any"
    },
    "comment": {
        "required": false,
        "type": "str",
        "comment": "Informational Comment about this Option and Value"
    },
    "example": {
        "required": false,
        "type": "any",
        "comment": "Example Data for this Option and Value"
    }
}