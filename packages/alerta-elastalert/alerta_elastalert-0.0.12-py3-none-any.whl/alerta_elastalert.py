from alerta.models.alert import Alert
from alerta.webhooks import WebhookBase
import json
from dateutil.parser import parse as parse_date

class ElastalertWebhook(WebhookBase):

    def incoming(self, query_string, payload):

        try:
            # Default parameters
            print("using alerta-elastalert version: 0.0.12")
            print("payload: "+str(payload))
            rawData = "data="+str(payload)
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
            attributes['payload']=str(payload)
            attributes['timestampReceived']=payload.get('@timestamp','N/A')
            try:
                createTime = parse_date(payload.get('@timestamp'))
            except Exception as e:
                print("unable to parse @timestamp as createTime")
                createTime = 'N/A'
            try:
                origin = payload['kubernetes']['host']
            except Exception as e:
                print("origin not defined")
                origin = 'N/A'
            print("Values being mapped: resource="+resource+",environment="+environment+",group="+group+",event="+event+",severity="+severity+",text="+text+",atributes="+str(attributes)+",createTime="+str(createTime)+",origin="+origin);
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
            type = "ElastAlertNotification",
            raw_data = "This is test",
            rawData = "Second Test"
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
