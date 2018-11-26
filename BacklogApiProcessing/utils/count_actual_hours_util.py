# -*- coding: utf-8 -*-
import json
import jmespath
from datetime import datetime, timedelta, timezone

class CountActualHoursUtil():
    def __init__(self, client, updated_since, updated_until, MAX_COUNT = 20):
        self.client =  client
        self.updated_since_dt =  datetime.strptime(updated_since, '%Y-%m-%d %H:%M:%S')
        self.updated_until_dt =  datetime.strptime(updated_until, '%Y-%m-%d %H:%M:%S')
        self.max_count =  MAX_COUNT

    def select_actual_hours(self, issueKey):
        query_params = {"count": self.max_count, "order": "asc"}  #TODO: over maxcount
        issue_comments = self.client.issue_comments(issueKey, query_params)  #sorted??
        updated_list = jmespath.search("[*].updated", issue_comments)
        original_value_list = []
        new_value_list = []
        #get first comments in term
        first_updated_index = self.__select_first_updated_index_in_term(updated_list)
        end_updated_index = self.__select_end_updated_index_in_term(updated_list)
        updated_list = updated_list[first_updated_index : end_updated_index + 1]
        issue_comments = issue_comments[first_updated_index : end_updated_index + 1]
        for i in range(len(updated_list)):
            search_actual_hours = "[" + str(i) + "]" + ".changeLog[?field=='actualHours']"
            search_new_value_str = search_actual_hours + ".newValue"
            search_original_value_str = search_actual_hours + ".originalValue"
            search_result_new_value_list = jmespath.search(search_new_value_str, issue_comments)
            search_result_original_value_list = jmespath.search(search_original_value_str, issue_comments)
            if len(search_result_original_value_list) > 0:
                #print(search_result_original_value_list[0])
                if search_result_original_value_list[0] != '':
                    original_value_list.append(search_result_original_value_list[0])
            if len(search_result_new_value_list) > 0:
                #print(search_result_new_value_list[0])
                if search_result_new_value_list[0] != '':
                    new_value_list.append(search_result_new_value_list[0])
            #original_value is None, and 
            if len(search_result_original_value_list) == 0 and len(search_result_new_value_list) > 0:
                if search_result_new_value_list[0] != '':
                    original_value_list.append(0)

        return self.__calculate_actual_hours(list(map(float, original_value_list)), list(map(float, new_value_list)))

    def __select_first_updated_index_in_term(self, updated_list):
        index = -1
        for i in range(len(updated_list)):
            item_updated_dt = datetime.strptime(updated_list[i], '%Y-%m-%dT%H:%M:%SZ')
            index = i
            if self.updated_since_dt <= item_updated_dt <= self.updated_until_dt:
                break
        return index

    def __select_end_updated_index_in_term(self, updated_list):
        index = -1
        for i in range(len(updated_list)):
            item_updated_dt = datetime.strptime(updated_list[i], '%Y-%m-%dT%H:%M:%SZ')
            if self.updated_since_dt <= item_updated_dt:
                if self.updated_since_dt <= item_updated_dt <= self.updated_until_dt:
                    index = i
                else:
                    break
        return index

    def __calculate_actual_hours(self, original_value_list, new_value_list):
        original_value = 0
        new_value = 0
        if len(original_value_list) > 0:
            original_value = original_value_list[0]
        if len(new_value_list) > 0:
            new_value = new_value_list[len(new_value_list) - 1]
        #print("original_value:" + str(original_value))
        #print("new_value:" + str(new_value))

        return new_value - original_value
