## Discord whatsapp bot

Don't get excited yet, this ******* only send a whatsapp message when someone connects in any voice chat.
`Thanks for this guy who made this https://github.com/chrishubert/whatsapp-web-api.git`; I just did a simple discord listener.


### How to log in whatsapp
1. Get containers up.
> docker compose up
2. Make a session on whatsapp web, go to: http://localhost:3000/session/start/DISC_WPP_SESSION

 Should return:
```json
{"success":true,"message":"Session initiated successfully"}
```
3. On your whatsapp_web_api container logs, it will appear a QRCODE, you already know what to do.
> docker logs whatsapp_web_api
4. You have to know the chat id or contact id you want to send the message, you can list contacts with:
> http://localhost:3000/client/getContacts/DISC_WPP_SESSION
```json
      {
         "id":{
            "server":"g.us",
            "user":"123123123123-123123123123",
            "_serialized":"123123123123-123123123123@g.us" #you need this
         },
         "number":null,
         "isBusiness":false,
         "isEnterprise":false,
         "name":"GROUP NAME OR CONTACT",
         "type":"in",
         "isMe":false,
         "isUser":false,
         "isGroup":true,
         "isWAContact":false,
         "isMyContact":false,
         "isBlocked":false
      }
```
5. Now you have to change the environment variables on docker-compose.yaml

| Key    | Value |
| -------- | ------- |
| CHAT_ID  | _serialized extracted from contacts |
| DISC_TOKEN | Your discord bot token (Make sure your bot have needed permissions) |

6. Now try (: