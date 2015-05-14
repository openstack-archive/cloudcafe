"""
Copyright 2013 Rackspace

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import json

from cafe.engine.models.base import \
    AutoMarshallingModel, AutoMarshallingListModel


class StacktachBaseListModel(AutoMarshallingListModel):

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """
        Returns an instance of a StackTach Deployments Response Entity
        based on the json serialized_str passed in.
        """
        results_list = json.loads(serialized_str)
        return cls._list_to_obj(results_list)

    @classmethod
    def _extract_data_from_list(cls, results_list, domain_model_type,
                                list_domain_model):
        """
        Helper method that creates a list domain model containing
        the singular form of the domina model.

        @note:
        Example response from a call to
        $stacktach_url/stacky/timings/?name=compute.instance.create

        [["compute.instance.create", "Time"],
        ["774b81da-4fa8-44ba-a86a-a9ab9b656536", "0d 00:00:00.36"],
        ["e8155b93-dafa-43ec-8cc8-21980c40bea3", "0d 00:00:00.42"],
        ...etc...]

        The first element is ["compute.instance.create", "Time"].
        This provides the 'header' or 'keys' information for all elements
        after the first element. So in the next element,
        "compute.instance.create"="774b81da-4fa8-44ba-a86a-a9ab9b656536" and
        "Time"= "0d 00:00:00.36" and so on.

        Also, this ordering is not consistent across all the models.
        Where they differ, _extract_data_from_list is overrided such as in
        WatchEvents.

        """

        if not results_list:
            raise Exception("Error: No data to parse through."
                            "Data contained: {1}".format(results_list))

        # first element contains one or more attribute names
        keys = results_list[0]
        key_count = len(keys)
        # data is contained after first element
        for result in results_list[1:]:
            entity_dict = {keys[i]: result[i] for i in range(key_count)}
            entity = domain_model_type._dict_to_obj(entity_dict)
            list_domain_model.append(entity)
        return list_domain_model


class EventName(AutoMarshallingModel):

    def __init__(self, event_name):
        """
        An object that represents a StackTack EventName Response Entity.
        """
        super(EventName, self).__init__()
        self.event_name = event_name

    @classmethod
    def _dict_to_obj(cls, entity_dict):
        """
        Helper method to turn dictionary into
        StackTach EventName Entity instance.
        """
        my_entity = EventName(
            event_name=entity_dict.get('Event Name'))
        return my_entity


class EventNames(StacktachBaseListModel):

    @classmethod
    def _list_to_obj(cls, results_list):
        return cls._extract_data_from_list(results_list=results_list,
                                           domain_model_type=EventName,
                                           list_domain_model=EventNames())


class HostName(AutoMarshallingModel):

    def __init__(self, host_name):
        """
        An object that represents a StackTack HostName Response Entity.
        """
        super(HostName, self).__init__()
        self.host_name = host_name

    @classmethod
    def _dict_to_obj(cls, entity_dict):
        """
        Helper method to turn dictionary into
        StackTach HostName Entity instance.
        """
        my_entity = HostName(
            host_name=entity_dict.get('Host Name'))
        return my_entity


class HostNames(StacktachBaseListModel):

    @classmethod
    def _list_to_obj(cls, results_list):
        return cls._extract_data_from_list(results_list=results_list,
                                           domain_model_type=HostName,
                                           list_domain_model=HostNames())


class Deployment(AutoMarshallingModel):

    def __init__(self, id, name):
        """
        An object that represents a StackTack Deployment Response Entity.
        """
        super(Deployment, self).__init__()
        self.id = id
        self.name = name

    @classmethod
    def _dict_to_obj(cls, entity_dict):
        """
        Helper method to turn dictionary into
        StackTach Deployment Entity instance.
        """
        my_entity = Deployment(
            id=entity_dict.get('#'),
            name=entity_dict.get('Name'))
        return my_entity


class Deployments(StacktachBaseListModel):

    @classmethod
    def _list_to_obj(cls, results_list):
        return cls._extract_data_from_list(results_list=results_list,
                                           domain_model_type=Deployment,
                                           list_domain_model=Deployments())


class TimingsSummary(AutoMarshallingModel):

    def __init__(self, event_name, count, minimum, maximum, average):
        """
        An object that represents a StackTack TimingsSummary Response Entity.
        """
        super(TimingsSummary, self).__init__()
        self.event_name = event_name
        self.count = count
        self.minimum = minimum
        self.maximum = maximum
        self.average = average

    @classmethod
    def _dict_to_obj(cls, entity_dict):
        """
        Helper method to turn dictionary into
        StackTach Deployment Entity instance.
        """
        my_entity = TimingsSummary(
            event_name=entity_dict.get('Event'),
            count=entity_dict.get('N'),
            minimum=entity_dict.get('Min'),
            maximum=entity_dict.get('Max'),
            average=entity_dict.get('Avg'))
        return my_entity


class TimingsSummaries(StacktachBaseListModel):

    @classmethod
    def _list_to_obj(cls, results_list):
        return cls._extract_data_from_list(
            results_list=results_list,
            domain_model_type=TimingsSummary,
            list_domain_model=TimingsSummaries())


class UuidTimingsSummary(AutoMarshallingModel):

    def __init__(self, state, event_name, timing):
        """
        An object that represents a StackTack UuidTimingsSummary
        Response Entity.
        """
        super(UuidTimingsSummary, self).__init__()
        self.state = state
        self.event_name = event_name
        self.timing = timing

    @classmethod
    def _dict_to_obj(cls, entity_dict):
        """
        Helper method to turn dictionary into
        StackTach UuidTimingsSummary Entity instance.
        """
        my_entity = UuidTimingsSummary(
            state=entity_dict.get('?'),
            event_name=entity_dict.get('Event'),
            timing=entity_dict.get('Time (secs)'))
        return my_entity


class UuidTimingsSummaries(StacktachBaseListModel):

    @classmethod
    def _list_to_obj(cls, results_list):
        return cls._extract_data_from_list(
            results_list=results_list,
            domain_model_type=UuidTimingsSummary,
            list_domain_model=UuidTimingsSummaries())


class EventNameTiming(AutoMarshallingModel):

    def __init__(self, timing, event_name):
        """
        An object that represents a StackTack EventNameTiming Response Entity.
        """
        super(EventNameTiming, self).__init__()
        self.event_name = event_name
        self.timing = timing

    @classmethod
    def _dict_to_obj(cls, entity_dict):
        """
        Helper method to turn dictionary into
        StackTach UuidTimingsSummary Entity instance.
        """
        my_entity = EventNameTiming(
            timing=entity_dict.pop('Time'),
            event_name=entity_dict.keys()[0])
        return my_entity


class EventNameTimings(StacktachBaseListModel):

    @classmethod
    def _list_to_obj(cls, results_list):
        return cls._extract_data_from_list(
            results_list=results_list,
            domain_model_type=EventNameTiming,
            list_domain_model=EventNameTimings())


class EventDetail(AutoMarshallingModel):

    def __init__(self, event_id, routing_key_type, when, deployment,
                 event_name, host_name, state, old_state, old_task):
        """
        An object that represents a StackTack EventDetail Response Entity.
        """
        super(EventDetail, self).__init__()
        self.event_id = event_id
        self.routing_key_type = routing_key_type
        self.when = when
        self.deployment = deployment
        self.event_name = event_name
        self.host_name = host_name
        self.state = state
        self.old_state = old_state
        self.old_task = old_task

    @classmethod
    def _dict_to_obj(cls, entity_dict):
        """
        Helper method to turn dictionary into
        StackTach EventDetail Entity instance.
        """
        my_entity = EventDetail(
            event_id=entity_dict.get('#'),
            routing_key_type=entity_dict.get('?'),
            when=entity_dict.get('When'),
            deployment=entity_dict.get('Deployment'),
            event_name=entity_dict.get('Event'),
            host_name=entity_dict.get('Host'),
            state=entity_dict.get('State'),
            old_state=entity_dict.get("State'"),
            old_task=entity_dict.get("Task'"))
        return my_entity


class EventDetails(StacktachBaseListModel):

    @classmethod
    def _list_to_obj(cls, results_list):
        return cls._extract_data_from_list(
            results_list=results_list,
            domain_model_type=EventDetail,
            list_domain_model=EventDetails())


class ImageEventDetail(AutoMarshallingModel):

    def __init__(self, event_id, routing_key_type, when,
                 deployment, event_name, host_name, status):
        """
        An object that represents a StackTack Image EventDetail Response Entity
        """
        super(ImageEventDetail, self).__init__()
        self.event_id = event_id
        self.routing_key_type = routing_key_type
        self.when = when
        self.deployment = deployment
        self.event_name = event_name
        self.host_name = host_name
        self.state = status

    @classmethod
    def _dict_to_obj(cls, entity_dict):
        """
        Helper method to turn dictionary into
        StackTach Image EventDetail Entity instance.
        """
        my_entity = ImageEventDetail(
            event_id=entity_dict.get('#'),
            routing_key_type=entity_dict.get('?'),
            when=entity_dict.get('When'),
            deployment=entity_dict.get('Deployment'),
            event_name=entity_dict.get('Event'),
            host_name=entity_dict.get('Host'),
            status=entity_dict.get('Status'))
        return my_entity


class ImageEventDetails(StacktachBaseListModel):

    @classmethod
    def _list_to_obj(cls, results_list):
        return cls._extract_data_from_list(
            results_list=results_list,
            domain_model_type=ImageEventDetail,
            list_domain_model=ImageEventDetails())


class KpiDetail(AutoMarshallingModel):

    def __init__(self, event_name, timing, uuid, deployment):
        """
        An object that represents a StackTack KpiDetail Response Entity.
        """
        super(KpiDetail, self).__init__()
        self.event_name = event_name
        self.timing = timing
        self.uuid = uuid
        self.deployment = deployment

    @classmethod
    def _dict_to_obj(cls, entity_dict):
        """
        Helper method to turn dictionary into
        StackTach KpiDetail Entity instance.
        """
        my_entity = KpiDetail(
            event_name=entity_dict.get('Event'),
            timing=entity_dict.get('Time'),
            uuid=entity_dict.get('UUID'),
            deployment=entity_dict.get('Deployment'))
        return my_entity


class KpiDetails(StacktachBaseListModel):

    @classmethod
    def _list_to_obj(cls, results_list):
        return cls._extract_data_from_list(
            results_list=results_list,
            domain_model_type=KpiDetail,
            list_domain_model=KpiDetails())


class WatchEvent(AutoMarshallingModel):

    def __init__(self, event_id, routing_key_type, when_date, when_time,
                 deployment, event_name, uuid):
        """
        An object that represents a StackTack WatchEvent Response Entity.
        """
        super(WatchEvent, self).__init__()
        self.event_id = event_id
        self.routing_key_type = routing_key_type
        self.when_date = when_date
        self.when_time = when_time
        self.deployment = deployment
        self.event_name = event_name
        self.uuid = uuid

    @classmethod
    def _dict_to_obj(cls, entity_dict):
        """
        Helper method to turn dictionary into
        StackTach WatchEvent Entity instance.
        """
        my_entity = WatchEvent(
            event_id=entity_dict.get(10),
            routing_key_type=entity_dict.get(1),
            when_date=entity_dict.get(15),
            when_time=entity_dict.get(20),
            deployment=entity_dict.get(50),
            event_name=entity_dict.get(36),
            uuid=entity_dict.get('UUID'))
        return my_entity


class WatchEvents(StacktachBaseListModel):

    @classmethod
    def _list_to_obj(cls, results_list):
        return cls._extract_data_from_list(
            results_list=results_list,
            domain_model_type=WatchEvent,
            list_domain_model=WatchEvents())

    @classmethod
    def _extract_data_from_list(cls, results_list, domain_model_type,
                                list_domain_model):
        """
        This overrided method is needed since there are more
        resultant data than the header data attribute names.
        """

        # first element contains one or more attribute names
        keys = results_list[0]
        key_count = len(keys)
        # data is contained after first element
        for result in results_list[1]:
            entity_dict = {keys[i]: result[i] for i in range(key_count)}
            entity_dict['UUID'] = result[key_count]
            entity = domain_model_type._dict_to_obj(entity_dict)
            list_domain_model.append(entity)
        return list_domain_model


class Report(AutoMarshallingModel):

    def __init__(self, report_id, start, end, created, name, version):
        """
        An object that represents a StackTack Report Response Entity.
        """
        super(Report, self).__init__()
        self.report_id = report_id
        self.start = start
        self.end = end
        self.created = created
        self.name = name
        self.version = version

    @classmethod
    def _dict_to_obj(cls, entity_dict):
        """
        Helper method to turn dictionary into
        StackTach Report Entity instance.
        """
        my_entity = Report(
            report_id=entity_dict.get('Id'),
            start=entity_dict.get('Start'),
            end=entity_dict.get('End'),
            created=entity_dict.get('Created'),
            name=entity_dict.get('Name'),
            version=entity_dict.get('Version'))
        return my_entity


class Reports(StacktachBaseListModel):

    @classmethod
    def _list_to_obj(cls, results_list):
        return cls._extract_data_from_list(
            results_list=results_list,
            domain_model_type=Report,
            list_domain_model=Reports())


class EventIdDetail(AutoMarshallingModel):

    def __init__(self, category, publisher, event_id, uuid, service, when,
                 host_name, state, deployment, event_name, request_id,
                 actual_event):
        """
        An object that represents a StackTack EventIdDetail Response Entity.
        """
        super(EventIdDetail, self).__init__()
        self.category = category
        self.publisher = publisher
        self.event_id = event_id
        self.uuid = uuid
        self.service = service
        self.when = when
        self.host_name = host_name
        self.state = state
        self.deployment = deployment
        self.event_name = event_name
        self.request_id = request_id
        self.actual_event = actual_event

    @classmethod
    def _dict_to_obj(cls, entity_dict):
        """
        Helper method to turn dictionary into
        StackTach EventIdDetail Entity instance.
        """
        my_entity = EventIdDetail(
            category=entity_dict.get('Category'),
            publisher=entity_dict.get('Publisher'),
            event_id=entity_dict.get('#'),
            uuid=entity_dict.get('UUID'),
            service=entity_dict.get('Service'),
            when=entity_dict.get('When'),
            host_name=entity_dict.get('Host'),
            state=entity_dict.get('State') or entity_dict.get('Status'),
            deployment=entity_dict.get('Deployment'),
            event_name=entity_dict.get('Event'),
            request_id=entity_dict.get('Req ID'),
            actual_event=entity_dict.get('actual_event'))
        return my_entity


class EventIdDetails(StacktachBaseListModel):

    @classmethod
    def _list_to_obj(cls, results_list):
        return cls._extract_data_from_list(
            results_list=results_list,
            domain_model_type=EventIdDetail,
            list_domain_model=EventIdDetails())

    @classmethod
    def _extract_data_from_list(cls, results_list, domain_model_type,
                                list_domain_model):
        """
        This overrided method is needed since the resultant data is
        organized differently.
        """
        # data is contained after first element
        entity_dict = {}
        for result in results_list[0][1:12]:
            entity_dict[result[0]] = result[1]
        entity_dict['actual_event'] = results_list[1]
        entity = domain_model_type._dict_to_obj(entity_dict)
        list_domain_model.append(entity)
        return list_domain_model
