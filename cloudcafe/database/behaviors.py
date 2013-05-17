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

import time
from datetime import datetime
from lxml import etree
from cafe.engine.behaviors import BaseBehavior
from cloudcafe.database.config import DBaaSConfig


class DatabaseAPI_Behaviors(BaseBehavior):
    def __init__(self, database_client=None):
        self._client = database_client
        self.config = DBaaSConfig()
        self.path_to_report = self.config.path_to_report
        self.path_to_error_report = self.config.path_to_error_report

    def create_active_instance(self,
                               client,
                               name="create_active_instance",
                               flavor_id=3,
                               volume=None,
                               databases=None,
                               users=None):
        """
        Create and active instance and validate it
        :param dbaasClient:
        :param name:
        :param flavor:
        :param volume:
        :return instance_id:
        """
        if volume is None:
            volume = {"size": 2}

        instance = client.instances.create(
            name=name,
            flavor_id=flavor_id,
            volume=volume,
            databases=databases,
            users=users
        )
        httpCode = self.get_last_response_code(client)
        if httpCode != '200':
            raise Exception("Create instance failed with code %s" % httpCode)
        instance_id = instance.id
        status, elapsed_time = self.wait_for_active(client,
                                                    instanceId=instance_id)
        if status == "ACTIVE":
            return instance_id, elapsed_time
        else:
            raise BaseException

    def create_perf_instance(self,
                             client,
                             flavorSize=3,
                             volumeSize=2):
        NAME = "create_perf_instance"
        FLAVOR = flavorSize
        VOLUME = volumeSize
        _db_name1 = "perfDB"
        _databases = [{"name": _db_name1}]
        _users = [{"name": "perfUser",
                   "password": "password2",
                   "databases": _databases}]
        instance = client.instances.create(
            name=NAME,
            flavor_id=FLAVOR,
            volume={"size": VOLUME},
            users=_users,
            databases=_databases)
        httpCode = self.get_last_response_code(client)
        if httpCode != '200':
            raise Exception("Create instance failed with code %s" % httpCode)
        instance_id = instance.id
        self.wait_for_active(client, instance_id)
        return instance_id

    def get_last_response_code(self, client):
        resp, body = client.client.last_response
        return str(resp.status)

    def wait_for_active(self,
                        client,
                        instanceId=None):
        """ Waiting for 'ACTIVE' status """
        status, elapsed_time = self.wait_for_status(client,
                                                    instanceId,
                                                    "ACTIVE")
        return status, elapsed_time

    def wait_for_status(self, client, instanceId, status):
        """ Waiting for passed-in status
        :rtype : status
        :rtype : elapsed_time
        @param dbaasClient:
        @param instanceId:
        @param status:
        """
        elapsed = 0
        startTime = time.time()
        current_status = self.get_instance_status(client,
                                                  instanceId=instanceId)
        while elapsed < 300:
            current_status = self.get_instance_status(client,
                                                      instanceId=instanceId)
            if current_status == status:
                return current_status, elapsed
            elif current_status == "ACTIVE":
                return "ACTIVE", elapsed
            elif current_status == "ERROR" or current_status == "FAILED":
                return "ERROR", elapsed
            else:
                time.sleep(10)
                elapsed = (time.time() - startTime)
        return current_status, elapsed

    def get_instance_status(self, client, instanceId=None):
        _instance = client.instances.get(instanceId)
        return _instance.status

    def get_instance_hostname(self, client, instanceId=None):
        _instance = client.instances.get(instanceId)
        return _instance.hostname

    def valid_duration(self, expected_timedelta,
                       single_event,
                       dateFormat):
        """Returns true if the event timedelta (endTime-startTime) is
        approximate to expected_timedelta (within error_margin_timedelta);
        expected_timedelta and error_margin_timedelta are timedelta objects"""

        error_margin_timedelta = 60
        startTimeStamp = datetime.strptime(single_event.startTime, dateFormat)
        endTimeStamp = datetime.strptime(single_event.endTime, dateFormat)
        event_delta = endTimeStamp - startTimeStamp

        #print("AH recorded time: %r" % event_delta.seconds)
        #print("Live test duration: %r" % expected_timedelta.seconds)
        return abs(
            event_delta.seconds -
            expected_timedelta.seconds) <= error_margin_timedelta

    def write_to_error_report(self,
                              instanceId,
                              exceptionMsg):
        instanceId = instanceId
        exception_msg = exceptionMsg

        try:
            open(self.path_to_error_report)
        #Create new report
        except:
            with open(self.path_to_error_report, 'w') as error_report_xml:
                error_report_header = etree.Element("error_details")
                error_report_xml.write(etree.tostring(error_report_header,
                                                      pretty_print=True))

        #Append to report
        try:
            parser = etree.XMLParser(remove_blank_text=True)
            tree = etree.parse(self.path_to_error_report, parser)
            error_header_root = tree.getroot()
            instanceId_element = etree.SubElement(error_header_root,
                                                  "Instance",
                                                  Id=instanceId)
            etree.SubElement(instanceId_element,
                             "exception_msg").text = exception_msg

            with open(self.path_to_error_report, 'w') as error_report_xml:
                error_report_xml.write(etree.tostring(tree,
                                                      pretty_print=True))
        except Exception as err:
            print (err)
            return False
        return True

    def write_to_report(self,
                        tc_name,
                        tc_pass=False):
        #Parse report to get root node
        try:
            open(self.path_to_report)
        except:
            with open(self.path_to_report, 'w') as report_xml:
                sbt_report_header = etree.Element("scenario_based_test")
                report_xml.write(etree.tostring(sbt_report_header,
                                                pretty_print=True))
        try:
            parser = etree.XMLParser(remove_blank_text=True)
            tree = etree.parse(self.path_to_report, parser)
            #Check to see if this test case exists
            tc_name_element_list = []
            try:
                tc_name_element_list = tree.xpath(
                    '//test_case[@name="' + tc_name + '"]')
            except Exception as err:
                print (err)
                #we didn't find the test case
                pass

            if len(tc_name_element_list) < 1:
                #create test case xml report block
                scenario_based_test_tag = tree.getroot()
                test_case_element = etree.SubElement(scenario_based_test_tag,
                                                     "test_case", name=tc_name)

                if tc_pass:
                    pass_num = etree.SubElement(test_case_element, "pass")
                    pass_num.text = "1"
                    fail_num = etree.SubElement(test_case_element, "fail")
                    fail_num.text = "0"
                else:
                    pass_num = etree.SubElement(test_case_element, "pass")
                    pass_num.text = "0"
                    fail_num = etree.SubElement(test_case_element, "fail")
                    fail_num.text = "1"

            else:
                tc_result_element = None
                result_total = 0
                if tc_pass:
                    tc_result_element = tree.xpath('//test_case[@name="' +
                                                   tc_name + '"]/pass')[0]
                    result_total = int(tree.xpath(
                        '//test_case[@name="' + tc_name + '"]/pass/text()')[0])
                else:
                    tc_result_element = tree.xpath('//test_case[@name="' +
                                                   tc_name + '"]/fail')[0]
                    result_total = int(tree.xpath(
                        '//test_case[@name="' + tc_name + '"]/fail/text()')[0])

                result_total += 1
                tc_result_element.text = str(result_total)
            with open(self.path_to_report, 'w') as f:
                f.write(etree.tostring(tree, pretty_print=True))
        except Exception as err:
            print (err)
            return False
        return True

    def wait_for_all_active(self, client, inst_id_list):
        """
        :param client:
        :param inst_id_list:
        :return:
        """
        for each_id in inst_id_list:
            self.wait_for_active(client,
                                 each_id)
        return True

    def is_instance_active(self,
                           client,
                           instanceStatus=None,
                           instanceId=None):
        if instanceStatus is not None:
            return instanceStatus == 'ACTIVE'
        if instanceId is not None:
            return self.get_instance_status(client,
                                            instanceId=instanceId) == 'ACTIVE'
        return False

    def found_resource(self,
                       client,
                       instanceId=None,
                       databaseName=None,
                       userName=None,
                       limit=1):
        """
        This method will run pagination every time since it
        limits its reply to 1 instance per list

        @param client:
        @param instanceId:
        @return: True if instance is found
        """
        instance_id = instanceId

        if databaseName:
            paginated_dbs = client.databases.list(instance_id, limit=limit)
            assert (len(paginated_dbs) <= limit)
            foundDB = False
            for _db in paginated_dbs:
                #print ("Instance id found: {0}".format(instanceId))
                if _db.name == databaseName:
                    #print ("Found instance with id {0}".format(_instance.id))
                    foundDB = True
                    break
                    #Check for pagination logic
            if foundDB is False:
                next_marker = paginated_dbs.next
                while next_marker is not None:
                    limit *= 2
                    paginated_dbs = client.databases.list(instance_id,
                                                          marker=next_marker,
                                                          limit=limit)
                    for _db in paginated_dbs:
                        if _db.name == databaseName:
                            foundDB = True
                            break
                    if foundDB is False:
                        next_marker = paginated_dbs.next
                    else:
                        break
            return foundDB
        if userName:
            paginated_users = client.users.list(instance_id, limit=limit)
            #TODO: put this assert back when pagination works
            assert (len(paginated_users) <= limit)
            foundUser = False
            for _user in paginated_users:
                #print ("Instance id found: {0}".format(instanceId))
                if _user.name == userName:
                    #print ("Found instance with id {0}".format(_instance.id))
                    foundUser = True
                    break
                    #Check for pagination logic
            if foundUser is False:
                next_marker = paginated_users.next
                while next_marker is not None:
                    limit *= 2
                    paginated_users = client.users.list(instance_id,
                                                        marker=next_marker,
                                                        limit=limit)
                    for _user in paginated_users:
                        #print ("Instance id found: {0}".format(_instance.id))
                        if _user.name == userName:
                            foundUser = True
                            break
                    if foundUser is False:
                        next_marker = paginated_users.next
                    else:
                        break
            return foundUser
        if instanceId:
            paginated_instances = client.instances.list(limit=limit)
            #TODO: put this assert back when pagination works
            assert (len(paginated_instances) <= limit)
            foundInstance = False
            for _instance in paginated_instances:
                #print ("Instance id found: {0}".format(instanceId))
                if _instance.id == instanceId:
                    #print ("Found instance with id {0}".format(_instance.id))
                    foundInstance = True
                    break
                    #Check for pagination logic
            if foundInstance is False:
                next_marker = paginated_instances.next
                while next_marker is not None:
                    limit *= 2
                    paginated_instances = client.instances.list(
                        marker=next_marker,
                        limit=limit)
                    for _instance in paginated_instances:
                        #print ("Instance id found: {0}".format(_instance.id))
                        if _instance.id == instanceId:
                            foundInstance = True
                            break
                    if foundInstance is False:
                        next_marker = paginated_instances.next
                    else:
                        break
            return foundInstance
