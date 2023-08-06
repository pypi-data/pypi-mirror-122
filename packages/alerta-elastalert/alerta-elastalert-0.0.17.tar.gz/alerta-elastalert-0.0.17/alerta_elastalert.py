from alerta.models.alert import Alert
from alerta.webhooks import WebhookBase
import json
from dateutil.parser import parse as parse_date
from datetime import datetime

class ElastalertWebhook(WebhookBase):

    def incoming(self, query_string, payload):

        try:
            #for any missing key in payload, default value set to 'N/A'
            print("using alerta-elastalert version: 0.0.17")
            print("payload: "+str(payload))
            rawData = "data="+str(payload)
            resource = payload.get('queryKey','N/A')
            environment = payload.get('fedUniqueName','N/A')
            res = payload.get('event','N/A')
            group = payload.get('group','N/A')
            #if event key present in payload, retrieve other nested key values
            if(res!="N/A"):
                event = res.get('eventName','N/A')
                severity =res.get('severity','unknown').lower()
                text = res.get('message','N/A')
            else:
                event = "N/A"
                severity = "unknown"
                text = "N/A"
            tags = []
            attributes = {}
            attributes['potentialImpact']=payload.get('potentialImpact','N/A')
            attributes['repairAction']=payload.get('repairAction','N/A')
            #parse @timestamp key field from string to datetime
            try:
                createTime = parse_date(payload.get('@timestamp'))
            except Exception as e:
            #if unable to parse or the key is missing, createTime will pick current time
                print("unable to parse @timestamp as createTime")
                createTime = datetime.now()
            try:
                origin = payload['kubernetes']['host']
            except Exception as e:
                print("origin not defined")
                origin = 'N/A'
            #logging values after being parsed
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
            create_time = createTime,
            attributes = attributes,
            environment = environment,
            event_type="ElastAlertNotification",
            raw_data = json.dumps(payload)
        )
