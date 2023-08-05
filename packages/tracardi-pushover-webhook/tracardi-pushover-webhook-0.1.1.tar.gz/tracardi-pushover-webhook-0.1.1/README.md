# Pushover plugin

This plugin sends a message to pushover service.

# Requirements

To use this plugin you must register at https://pushover.net and obtain API_TOKEN and USER_KEY.

# Configuration

```json
{
  "api_token": "API_TOKEN from PushOver",
  "user_key": "USER_KEY from PushOver",
  "message": "Message"
}
```

# Input

This plugin does not take any input

# Output

Output returns status and response body form PushOver service. 

```json
{
  "status": 200,
  "body": {
    "status": 1,
    "request": "c759f16e-c10a-4066-b91d-05fd06504790"
  }
}
```
