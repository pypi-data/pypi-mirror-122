
from alerta.models.alert import Alert
from alerta.webhooks import WebhookBase
import json

class ElastalertWebhook(WebhookBase):

    def incoming(self, query_string, payload):

        try:
            # Default parameters
            print("payload: "+str(payload))
            rawData = str(payload)
            resource = payload.get('queryKey','N/A')
            environment = payload.get('fedUniqueName','N/A')
            res = payload.get('event','N/A')
            group = payload.get('group','N/A')
            if(res!="N/A"):
                event = res.get('eventName','N/A')
                severity =res.get('severity','N/A').lower()
                text = res.get('message','N/A')
            else:
                event = "N/A"
                severity = "N/A"
                text = "N/A"
            tags = []
            attributes = {}
            attributes['potentialImpact']=payload.get('potentialImpact','N/A')
            attributes['remedy']=payload.get('remedy','N/A')
            attributes['rawData']=str(payload)
            createTime = payload.get('@timestamp','N/A')
            try:
                origin = payload['kubernetes']['host']
            except Exception as e:
                print("origin not defined")
                origin = 'N/A'
        except Exception as e:
            print("Error reading payload: "+str(e)) 

        return Alert(
            resource = resource,
            event = event,
            severity = severity,
            service = [],
            group = group,
            text = text,
            tags = tags,
            origin = origin,
            createTime = createTime,
            attributes = attributes,
            environment = environment,
            rawData = rawData
        #     environment=payload.get('environment', environment),
        #     severity=payload.get('severity', severity),
        #     service=['fail2ban'],
        #     group=payload.get('group', group),
        #     value='BAN',
        #     text=payload.get('message', text),
        #     tags=payload.get('tags', tags),
        #     attributes=payload.get('attributes', attributes),
        #     origin=payload.get('hostname', origin),
        #     raw_data=json.dumps(payload, indent=4)
        )

        # return Alert(
        #     resource=payload['resource'],
        #     event=payload['event'],
        #     environment=payload.get('environment', environment),
        #     severity=payload.get('severity', severity),
        #     service=['fail2ban'],
        #     group=payload.get('group', group),
        #     value='BAN',
        #     text=payload.get('message', text),
        #     tags=payload.get('tags', tags),
        #     attributes=payload.get('attributes', attributes),
        #     origin=payload.get('hostname', origin),
        #     raw_data=json.dumps(payload, indent=4)
        # )   
