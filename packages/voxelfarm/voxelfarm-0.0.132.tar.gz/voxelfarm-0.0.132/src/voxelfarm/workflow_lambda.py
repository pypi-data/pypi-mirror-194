import requests
import os
import os.path
import glob
import datetime
import time
from random import *
import csv 
import pandas as pd
import json
import base64
import voxelfarm
from voxelfarm import voxelfarmclient

def _handle_non_serializable(obj):
    return None

class state:
    initialize = 0
    receive_data = 1
    stage_done = 2

class request:
    def __init__(self, framework, vf):
        framework.log('Creating request...')

        self.vf_api = vf
        self.lambda_framework = framework

        self.project_id = framework.input_string('project_id', 'Project Id', '')
        self.version_folder_id = framework.input_string('version_folder_id', 'Version Folder', '')

        self.update_type = framework.update_type()
        self.stage_done = framework.stage_done()

        self.state = state.initialize
        if self.version_folder_id:
            if self.stage_done:
                self.state = state.stage_done
            else:
                self.state = state.receive_data

        self.crs = {}
        # Get the coordinate system of the project
        framework.log('Retrieving project CRS...')
        result = self.vf_api.get_project_crs(self.project_id)
        if result.success:
            self.crs = result.crs
            framework.log('Retrieved project CRS')

        framework.log(f'state {self.state}')
        framework.log(f'project_id {self.project_id}')

        if self.state == state.initialize:
            self.raw_entity_id = None
            self.product_id = None
            self.product_folder_id = None
            self.user = None
            self.comment = None
            self.capture_date = None
            self.entity_id = None
        else:
            self.scrap_folder = framework.get_scrap_folder()          

            entity = framework.get_entity()
            self.entity_id = entity['ID']

            framework.log(f'entity_id {self.entity_id}')

            self.raw_entity_id = framework.input_string('raw_entity_id', 'Entity Id', '')
            self.product_id = framework.input_string('product_id', 'Product Id', '')
            self.product_folder_id = framework.input_string('product_folder_id', 'Product Folder', '')
            self.user = framework.input_string('user', 'User', '')
            self.comment = framework.input_string('comment', 'Comment', '')
            self.capture_date = framework.input_string('capture_date', 'Capture Date', '')

            framework.log(f'scrap_folder {self.scrap_folder}')
            framework.log(f'raw_entity_id {self.raw_entity_id}')
            framework.log(f'product_id {self.product_id}')
            framework.log(f'product_folder_id {self.product_folder_id}')
            framework.log(f'version_folder_id {self.version_folder_id}')
            framework.log(f'user {self.user}')
            framework.log(f'comment {self.comment}')
            framework.log(f'capture_date {self.capture_date}')
            framework.log(f'update_type {self.update_type}')
            framework.log(f'stage_done {self.stage_done}')

            product_entity = self.vf_api.get_entity(self.product_folder_id, self.project_id)
            framework.log(f'product_entity:{product_entity}')

            # Load previously active version properties
            framework.log('Loading properties from active version...')

            self.active_version_folder_id = "0"
            self.active_version_properties = {}
            if (product_entity and 'version_active' in product_entity and product_entity['version_active'] != '0'):
                self.active_version_folder_id = product_entity['version_active']
                active_version_entity = self.vf_api.get_entity(self.active_version_folder_id, self.project_id)
                if active_version_entity:
                    for prop in active_version_entity:
                        if prop.find('version_') == 0:
                            value = active_version_entity[prop]
                            prop_name = prop.replace('version_', '', 1)
                            self.active_version_properties[prop_name] = value

            # Load version properties
            framework.log('Loading properties from current version...')
            self.properties = {}
            version_entity = self.vf_api.get_entity(self.version_folder_id, self.project_id)
            if version_entity:
                for prop in version_entity:
                    if prop.find('version_') == 0:
                        value = version_entity[prop]
                        prop_name = prop.replace('version_', '', 1)
                        prop_value = version_entity[prop]
                        self.properties[prop_name] = prop_value
                        framework.log(f'{prop_name} = {prop_value}')

    def get_client_api(self):
        return self.vf_api        

    def get_product_property(self, product_id, property):
        self.lambda_framework.log(f'getting {product_id} property:{property}...')

        workflow_entity = self.vf_api.get_entity(self.project_id, self.project_id)

        field_id = f'workflow_folder_{product_id}'
        if workflow_entity and (field_id in workflow_entity):
            product_folder_id = workflow_entity[field_id]
            self.lambda_framework.log(f'product_folder_id:{product_folder_id}')

            product_entity = self.vf_api.get_entity(product_folder_id, self.project_id)
            if product_entity:
                self.lambda_framework.log(f'product_entity:{product_entity}')
                active_version_id = product_entity['version_active']
                active_version = self.vf_api.get_entity(active_version_id, self.project_id)
                self.lambda_framework.log(f'active_version:{active_version}')
                extended_prop = 'version_' + property
                self.lambda_framework.log(f'extended_prop:{extended_prop}')
                if active_version != None and extended_prop in active_version:
                    return active_version[extended_prop]

        return None

    def get_product_singleton(self, product_id, singleton_id):
        self.lambda_framework.log(f'getting {singleton_id} for {product_id}...')

        workflow_entity = self.vf_api.get_entity(self.project_id, self.project_id)

        field_id = f'workflow_folder_{product_id}'
        if workflow_entity and (field_id in workflow_entity):
            product_folder_id = workflow_entity[field_id]
            self.lambda_framework.log(f'product_folder_id:{product_folder_id}')
            
            product_entity = self.vf_api.get_entity(product_folder_id, self.project_id)
            if product_entity:
                self.lambda_framework.log(f'product_entity: {product_entity}')
                singleton_property = f'workflow_singleton_{singleton_id}'
                if product_entity and singleton_property in product_entity:
                    return product_entity[singleton_property]

        return None

    def define_product_alias(self, alias, value):
        self.lambda_framework.log(f'Define alias {alias} for product {self.product_id}')
        updatedProperties = {}
        alias_property_id = 'alias_' + alias
        updatedProperties[alias_property_id] = value

        self.vf_api.update_entity(
            project=self.project_id,
            id=self.version_folder_id,
            fields=updatedProperties
        )

    def get_callback(self, update_type : str):
        if update_type:
            return f'{self.entity_id}/{update_type}'
        
        return None

class workflow_lambda_framework:

    def __init__(self):  
        pass

    def input_string(self, id, label, default = ""):
        return ""

    def log(self, message):
        pass

    def progress(self, progress, message):
        pass

    def get_entity(self, id = None):
        return None

    def download_entity_file(self, filename, id = None):
        return ""
    
    def get_scrap_folder(self):
        return ""

    def get_tools_folder(self):
        return ""

    def get_entity_folder(self, id = None):
        return ""

    def download_entity_files(self, id = None):
        return ""

    def download_entity_file(self, filename, id = None):
        return ""

    def attach_file(self, filename, id = None):
        pass

    def attach_folder(self, folder, id = None):
        pass

    def upload(self, filename, name, id = None):
        pass

    def set_exit_code(self, code):
        pass

    def get_entity_file_list(self, id = None):
        return []
    
    def update_type(self):
        return None

    def stage_done(self):
        return False

    def get_vf_api(self):
        return None

    def increment_counter(self, counter, offset = 1):
        return 0
    
    def decrement_counter(self, counter, offset = 1):
        return 0

    def set_counter(self, counter, value = 0):
        pass

    def get_working_dir(self):
        return ''

    def get_notify_emails(self):
        return ''

    def get_notify_users_url(self):
        return ''

    def get_workflow_api(self):
        return ''

    def publish_feed(self, filename):
        return {'success': True}

class workflow_lambda_host:

    def __init__(self, framework = None):  
        if framework:
            self.lambda_framework = framework
        else:
            if voxelfarm.voxelfarm_framework:
                self.lambda_framework = voxelfarm.voxelfarm_framework
            else:
                self.lambda_framework = workflow_lambda_framework()

        self.vf_api = self.lambda_framework.get_vf_api()
        if not self.vf_api:
            self.vf_api = voxelfarmclient.rest('http://localhost')

    def input_string(self, id, label, default = ""):
        return self.lambda_framework.input_string(id, label, default)

    def log(self, message):
        self.lambda_framework.log(message)

    def progress(self, progress, message):
        self.lambda_framework.progress(progress, message)

    def get_scrap_folder(self):
        return self.lambda_framework.get_scrap_folder()

    def get_tools_folder(self):
        return self.lambda_framework.get_tools_folder()

    def get_entity_folder(self, id = None):
        return self.lambda_framework.get_entity_folder(id)

    def download_entity_files(self, id = None):
        return self.lambda_framework.download_entity_files(id)

    def download_entity_file(self, filename, id = None):
        return self.lambda_framework.download_entity_file(filename, id)

    def attach_file(self, filename, id = None):
        self.lambda_framework.attach_file(filename, id)

    def attach_folder(self, folder, id = None):
        self.lambda_framework.attach_folder(folder, id)

    def upload(self, filename, name, id = None):
        self.lambda_framework.Upload(filename, name, id)

    def set_exit_code(self, code):
        self.lambda_framework.set_exit_code(code)

    def get_entity(self, id = None):
        return self.lambda_framework.get_entity(id)

    def get_entity_file_list(self, id = None):
        return self.lambda_framework.get_entity_file_list(id)

    def update_type(self):
        if self.lambda_framework.stage_done():
            return self.lambda_framework.get_callback_update_type()
        
        return None

    def stage_done(self):
        return self.lambda_framework.stage_done()

    def increment_counter(self, counter, offset = 1):
        return self.lambda_framework.increment_counter(counter, offset)
    
    def decrement_counter(self, counter, offset = 1):
        return self.lambda_framework.decrement_counter(counter, offset)

    def set_counter(self, counter, value = 0):
        self.lambda_framework.set_counter(counter, value)

    def get_working_dir(self):
        return self.lambda_framework.get_working_dir()
    
    def get_notify_emails(self):
        return self.lambda_framework.get_notify_emails()

    def get_notify_users_url(self):
        return self.lambda_framework.get_notify_users_url()

    def get_workflow_api(self):
        return self.lambda_framework.get_workflow_api()

    def find_product_definition(self, product, workflow):
        if 'id' in workflow:
            product_id = workflow['id']
            self.lambda_framework.log(f'product_id: {product_id}')

            if product_id == product:
                return workflow
            else:
                if 'tracks' in workflow:
                    for track in workflow['tracks']:
                        self.lambda_framework.log(f'track: {track}')

                        product_definition = self.find_product_definition(product, track)
                        if product_definition:
                            return product_definition

        return None

    def _is_number(self, element) -> bool:
        try:
            float(element)
            return True
        except:
            return False

    def _create_workflow_folders(self, vf, workflow, project_id, project_entity, parent_folder, fields, crs):
        result = vf.api_result()

        if 'singletons' in workflow:
            existing_version = vf.get_entity(parent_folder, project_id)
            existing_singleton_ids = {}
            if existing_version:
                for prop in existing_version:
                    if prop.startswith('workflow_singleton_'):
                        existing_singleton_ids[prop] = existing_version[prop]

            singleton_ids = {}
            for singleton in workflow['singletons']:
                create_singleton = False    
                singleton_key = f'workflow_singleton_{singleton}'
                if singleton_key in existing_singleton_ids:
                    singleton_id = existing_singleton_ids[singleton_key]
                    singleton_entity = vf.get_entity(singleton_id, project_id)
                    if singleton_entity == None:
                        create_singleton = True    
                else:
                    create_singleton = True    
                    
                if create_singleton:    
                    self.lambda_framework.log(f'Creating Product singleton {workflow["id"]} {parent_folder} {singleton}...')
                    api_result = vf.create_entity_raw(
                        project=project_id, 
                        type='RAW', 
                        name=f'{singleton}', 
                        fields={
                            'file_folder': parent_folder,
                            'capture_date' : str(1000 * int(time.time()))
                        },
                        crs=crs)
                    
                    if not api_result.success:
                        return api_result
                    
                    singleton_id = api_result.id
                    singleton_ids[f'workflow_singleton_{singleton}'] = singleton_id
                    self.lambda_framework.log(f'Created Raw Singleton {singleton_id}')

            if singleton_ids:
                vf.update_entity(
                    project=project_id, 
                    id=parent_folder, 
                    fields=singleton_ids)

        if 'tracks' in workflow:
            for track in workflow['tracks']:
                product_id = track['id']
                field_id = f'workflow_folder_{product_id}'
                if field_id in project_entity:
                    folder_id = project_entity[field_id]
                    folder = vf.get_entity(folder_id, project_id)
                    if folder != None:
                        api_result = self._create_workflow_folders(vf, track, project_id, project_entity, folder_id, fields, crs)
                        if not api_result.success:
                            return api_result
                        
                        continue
                    else:        
                        self.lambda_framework.log(f'folder does not exists: {folder}')    
                else:
                    self.lambda_framework.log(f'field_id does not exists: {field_id}')    

                track_name = track['name']
                self.lambda_framework.log(f'Creating Product folder {product_id} {parent_folder} {track_name}...')
                api_result = vf.create_folder(
                    project=project_id, 
                    folder=parent_folder,
                    name=track['name'],
                    fields={
                        'workflow_product' : product_id,
                        'version_last' : '0',
                        'version_active' : '0'
                    })
                
                if not api_result.success:
                    return api_result
                
                sub_folder_id = api_result.id

                fields[field_id] = sub_folder_id
                self.lambda_framework.log('Created Product folder')
                api_result = self._create_workflow_folders(vf, track, project_id, project_entity, sub_folder_id, fields, crs)
                if not api_result.success:
                    return api_result
        
        result.success = True
        return result    

    def set_workflow_definition(self, workflow_definition):
        self.lambda_framework.log('Create workflow request')

        result = {
            'success': False,
            'error_info': '',
            'complete': False}

        workflow_request = request(self.lambda_framework, self.vf_api)

        if workflow_request.state == state.initialize:
            self.lambda_framework.log('Initialize workflow')
            project_entity = self.vf_api.get_entity(workflow_request.project_id, workflow_request.project_id)

            encoded_workflow = json.dumps(workflow_definition, default=_handle_non_serializable)
            encoded_bytes = encoded_workflow.encode('ascii')
            encoded_bytes = base64.b64encode(encoded_bytes)
            encoded_workflow = encoded_bytes.decode('ascii')

            fields = {
                'workflow' : encoded_workflow
            }

            self.lambda_framework.log('Creating Workflow Folders')
            api_result = self._create_workflow_folders(self.vf_api, workflow_definition, workflow_request.project_id, project_entity, '0', fields, workflow_request.crs)

            if api_result.success:
                self.lambda_framework.log(fields)
                self.lambda_framework.log(f'Saving changes to project {workflow_request.project_id}...')

                api_result = self.vf_api.update_entity(
                    project=workflow_request.project_id, 
                    id=workflow_request.project_id, 
                    fields=fields)

                if api_result.success:
                    result['success'] = True
                    result['complete'] = True
                else:        
                    self.lambda_framework.log('Error updating project.')
                    result['error_info'] = api_result.error_info
            else:        
                self.lambda_framework.log('Creating workflow folder failed.')
                result['error_info'] = api_result.error_info
        else:
            self.lambda_framework.log(f'Find product definition: {workflow_request.product_id}')
            product_definition = self.find_product_definition(workflow_request.product_id, workflow_definition)
            if product_definition:
                workflow_complete = False
                if workflow_request.state == state.stage_done:
                    if 'on_stage_done' in product_definition:
                        self.lambda_framework.log('Execute on_stage_done event')
                        event_result = product_definition['on_stage_done'](self.vf_api, workflow_request, self)

                        if event_result:
                            if 'success' in event_result:
                                if event_result['success']:
                                    self.lambda_framework.log('Done for on_stage_done event')
                                    if "complete" in event_result and event_result["complete"]:
                                        workflow_complete = True
                                else:    
                                    if 'error_info' in event_result:
                                        self.lambda_framework.log('Error in on_stage_done event: ' + result['error_info'])
                                    else:
                                        result['error_info'] = 'Unknown error'
                            else:
                                result['error_info'] = 'on_stage_done success result not found'
                        else:        
                            result['error_info'] = 'on_stage_done return no data'
                    else:
                        result['error_info'] = 'on_stage_done event not defined'
                elif workflow_request.state == state.receive_data:    
                    if 'on_receive_data' in product_definition:
                        self.lambda_framework.log('Execute on_receive_data event')
                        event_result = product_definition['on_receive_data'](self.vf_api, workflow_request, self)

                        if event_result:
                            if 'success' in event_result:
                                if event_result['success']:
                                    self.lambda_framework.log('Done for on_receive_data event')

                                    if "complete" in event_result and event_result["complete"]:
                                        workflow_complete = True
                                else:    
                                    if 'error_info' in event_result:
                                        result['error_info'] = event_result['error_info']
                                    else:
                                        result['error_info'] = 'Unknown error'
                            else:
                                result['error_info'] = 'on_receive_data success result not found'
                        else:
                            result['error_info'] = 'on_receive_data return no data'
                    else:
                        result['error_info'] = 'on_receive_data event not defined'
                else:
                    self.lambda_framework.log('Unknown workflow state')
                    result['error_info'] = 'Unknown workflow state'
                    return result

                # Auto-activate version
                if workflow_complete and not 'activated' in workflow_request.properties:
                    self.lambda_framework.log(f'Updating product version_active folder...{workflow_request.product_folder_id}')
                    product_entity = self.lambda_framework.get_entity(workflow_request.product_folder_id)

                    if product_entity and product_entity.ContainsKey('version_active'):
                        previous_active_version = product_entity['version_active'] 
                        if previous_active_version == '':
                            previous_active_version = '0'
                        self.lambda_framework.log(f'Previously active version: {previous_active_version}')
                        api_result = self.vf_api.update_entity(
                            project=workflow_request.project_id,
                            id=workflow_request.product_folder_id,
                            fields={
                                'version_active' : str(workflow_request.version_folder_id)
                            }
                        )

                        if not api_result.success:
                            result['error_info'] = api_result.error_info

                        workflow_request.properties['activated'] = '1'
                        self.lambda_framework.log('Updated product active_version.')        
                    else:
                        self.lambda_framework.log(f'product_entity: {workflow_request.product_folder_id} not found')

                # write properties
                self.lambda_framework.log(f'Saving properties...{workflow_request.project_id}...{workflow_request.version_folder_id}')
                updatedProperties = {}
                for prop in workflow_request.properties:
                    version_property_id = 'version_' + prop
                    property_value = workflow_request.properties[prop]
                    updatedProperties[version_property_id] = property_value
                    self.lambda_framework.log(f'{version_property_id} = {property_value}')

                api_result = self.vf_api.update_entity(
                    project=workflow_request.project_id,
                    id=workflow_request.version_folder_id,
                    fields=updatedProperties  
                )   

                if api_result.success:
                    self.lambda_framework.log('Done saving properties')
                else:
                    self.lambda_framework.log(f'Error saving properties: {api_result.error_info}')
            else:
                self.lambda_framework.log('Product definition not found')
                result['error_info'] = 'Product definition not found'

            self.lambda_framework.log('Done set_workflow_definition')

        if 'success' in result and result['success']:
            if "complete" in result and result["complete"]:
                self.lambda_framework.log("workflow_lambda Done")
                self.lambda_framework.set_exit_code(0)
            else:
                self.lambda_framework.log("workflow_lambda Partial")
        else:
            self.lambda_framework.log("workflow_lambda Error: " + result['error_info'])
            self.lambda_framework.set_exit_code(1)

    def get_product_singleton(self, product_id, singleton_id):
        self.lambda_framework.log(f'getting {singleton_id} for {product_id}...')

        entity = self.lambda_framework.get_entity()
        if entity and entity.ContainsKey('project'):
            project_id = entity['project']
            project_entity = self.lambda_framework.get_entity(project_id)

            field_id = f'workflow_folder_{product_id}'
            if project_entity and project_entity.ContainsKey(field_id):
                product_folder_id = project_entity[field_id]
                self.lambda_framework.log(f'product_folder_id:{product_folder_id}')

                if product_entity:
                    product_entity = self.vf_api.get_entity(product_folder_id)
                    self.lambda_framework.log(f'product_entity: {product_entity}')

                    singleton_property = f'workflow_singleton_{singleton_id}'
                    if product_entity and product_entity.ContainsKey(singleton_property):
                        return product_entity[singleton_property]
        else:
            self.lambda_framework.log('Project not found in entity.')

        return None

    def get_product_property(self, product_id, property):
        self.lambda_framework.log(f'getting {product_id} property:{property}...')

        entity = self.lambda_framework.get_entity()
        if entity and entity.ContainsKey('project'):
            project_id = entity['project']
            project_entity = self.lambda_framework.get_entity(project_id)

            if project_entity and project_entity.ContainsKey('workflow_folder_' + product_id):
                product_folder_id = project_entity['workflow_folder_' + product_id]
                product_entity = self.lambda_framework.get_entity(product_folder_id)
                if product_entity and product_entity.ContainsKey('version_active'):
                    active_version_id = product_entity['version_active']
                    active_version = self.lambda_framework.get_entity(active_version_id)
                    extended_prop = 'version_' + property
                    if active_version and active_version.ContainsKey(extended_prop):
                        return active_version[extended_prop]
                    else:
                        self.lambda_framework.log('Problem with entity active_version ' + active_version_id)
                else:
                    self.lambda_framework.log('Problem with entity product_entity ' + product_folder_id)
            else:
                self.lambda_framework.log('Problem with entity project ' + project_id)
        else:
            self.lambda_framework.log('Project not found in entity.')

        return None

    def get_parameter_dataframe(self, product_id):
        attribute_product = self.get_product_property(product_id, 'report_entity')
        if attribute_product:
            attribute_file = self.lambda_framework.download_entity_file('report.csv', attribute_product)
            if os.path.isfile(attribute_file):
                return pd.read_csv(attribute_file)
            else:
                self.lambda_framework.log('Parameter file not found.')
        else:
            self.lambda_framework.log('Attribute product not found.')

        return pd.DataFrame()

    def load_feed(self, workflow_request: request, entity_id:str):
        self.lambda_framework.log(f'load_feed {entity_id}...')
        entity_path = self.download_entity_files(entity_id)
        if not os.path.isdir(entity_path):
            self.lambda_framework.log('Error Raw product empty')
            return {'success': False}

        self.lambda_framework.log(f'Raw Entity loaded successfully {entity_path}')
        
        types = ('*.ftr', 'report.csv')
        entity_files = []
        for files in types:
            entity_files.extend(glob.glob(entity_path + "\\" + files))

        self.lambda_framework.log(f'entity_files:{entity_files}')

        for file_name in entity_files:
            entity_file = os.path.join(workflow_request.scrap_folder, file_name)
            self.lambda_framework.log(f'feed file:{entity_file}')
            if entity_file:
                if file_name.endswith('.ftr'):
                    df_model = pd.read_feather(entity_file)
                elif file_name.endswith('.csv'):
                    df_model = pd.read_csv(entity_file)
                else:
                    self.lambda_framework.log(f'Unsupported file type {file_name}')
                    return {'success': False}
                if not df_model.empty:
                    return {'success': True, 'df': df_model}
                else:           
                    self.lambda_framework.log(f'file {file_name} is empty.')
                    return {'success': False}

    def publish_reports(self, workflow_request: request, report_name:str, report_id: str, constant_spatial_id: str, constant_object_id: str, propertyIds:tuple, timestampID: str = None, spatialId: str = None, objectId: str = None):
        self.lambda_framework.log(f'Publish reports calling timeseries')
        self.lambda_framework.log(f'report_id:{report_id}')

        propertyStr = ''
        for val in propertyIds:
            propertyStr += ','.join(map(str, val)) + "|"

        self.lambda_framework.log(f'propertyStr:{propertyStr}')
        self.lambda_framework.log(f'Calling process entity to publish report {report_id}...')
        mesh_entity = self.lambda_framework.get_entity(report_id)
        if not mesh_entity:
            self.lambda_framework.log(f'Error getting mesh_entity {report_id}')
            return {'success': False, 'error_info': 'Error getting mesh_entity'}
        file_date = mesh_entity['file_date']
        self.lambda_framework.log(f'mesh_entity.file_date:{file_date}')
        iso_time = datetime.datetime.fromtimestamp(int(file_date)/1000.0).isoformat()
        self.lambda_framework.log(f'mesh_entity.iso_time:{iso_time}')
        result = self.load_feed(workflow_request, report_id)
        if not result['success']:
            return {'success': False, 'error_info': 'load_feed failed'}
        self._handle_dataframe(workflow_request, result['df'], report_id, f"{iso_time}", timestampID, spatialId, objectId, propertyIds, constant_spatial_id, constant_object_id)
        self.lambda_framework.log(f'End process for report {report_id}')    
        return {'success': True}

    def _handle_dataframe(self, workflow_request: request, df_model:pd.DataFrame, report_id: str, timestamp:str, timestampId:str, spatialId: str, objectId: str, propertyIds:tuple, constant_spatial_id:str, constant_object_id:str):
        self.lambda_framework.log(f'handle_dataframe:timestamp:{timestamp}|timestampId:{timestampId}|spatialId:{spatialId}|objectId:{objectId}|constant_spatial_id:{constant_spatial_id}|constant_object_id:{constant_object_id}')
        self.lambda_framework.log(df_model.dtypes.to_string())
        self.lambda_framework.log(df_model.head().to_string())
        if timestampId in df_model or timestamp is not None:
            eventsToSend = []
            for idx, row in df_model.iterrows():
                valid = False   
                spatial_value = '-'
                if spatialId and spatialId in row:
                    spatial_value = row[spatialId]
                    valid = True
                elif constant_spatial_id and constant_object_id:
                    valid = True
                
                object_value = '-'
                if objectId and objectId in row:
                    object_value = row[objectId]
                    valid = True

                if valid:
                    if timestampId:
                        try:
                            timestamp = str(row[timestampId])
                            if timestamp is 'None' or timestamp.strip() == '':
                                self.lambda_framework.log(f'Mandatory timestamp value is empty for {row}. Please check the input file. Skipping this row.')
                                continue
                            if " " in timestamp:
                                if "AM" or "PM" in timestamp:
                                    entry_date = time.mktime(datetime.datetime.strptime(timestamp, "%d/%m/%Y %H:%M:%S %p").timetuple())
                                else: 
                                    entry_date = time.mktime(datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").timetuple())
                            else:
                                entry_date = time.mktime(datetime.datetime.strptime(timestamp, "%Y-%m-%d").timetuple())
                            iso_time = datetime.datetime.fromtimestamp(entry_date).isoformat()
                        except:
                            self.lambda_framework.log(f'Something went wrong converting the date for {timestamp}. Row:{row}. Please check the input file. Skipping this row.')
                            continue
                    else:
                        iso_time = timestamp

                    eventObj = {
                        "time": iso_time,
                        "spatialId": constant_spatial_id if constant_spatial_id != '' else spatial_value, 
                        "objectId": constant_object_id if constant_object_id != '' else object_value,
                    }
                    validPropertyValueFound = False
                    for propertyId in propertyIds:
                        if propertyId[0] in df_model:
                            validPropertyValueFound = True
                            eventObj[propertyId[1]] = float(row[propertyId[0]]) if self._is_number(row[propertyId[0]]) else (row[propertyId[0]] if not pd.isnull(row[propertyId[0]]) else '')

                    if validPropertyValueFound:
                        eventsToSend.append(eventObj)
                        #if idx % 250 == 0:
                            #self.lambda_framework.log(f'event to send JSON :{json.dumps(eventObj)}')
                            
            self.lambda_framework.log(f'eventsToSend count:{len(eventsToSend)}')
            if len(eventsToSend) > 0:
                self.lambda_framework.log(f'first event from the list to send to Time Series: {json.dumps(eventsToSend[0])}')

            filename = f"dump_tsi_{report_id}.csv"
            df_dump = pd.DataFrame(eventsToSend) 
            df_dump.to_csv(os.path.join(workflow_request.scrap_folder, filename), index=False)
            self.lambda_framework.publish_feed(filename)
        else:
            self.lambda_framework.log(timestampId + ' column not found in dataframe or "timestamp" value was empty (' + timestamp + ').')

    def _get_file_path(self, file):
        if os.path.exists(file):
            return file
        else:
            script_dir = self.lambda_framework.get_working_dir()
            self.lambda_framework.log('file is a relative path')
            file_path = os.path.join(script_dir, file)

            if os.path.exists(file_path):
                return file_path
    
        return None

    def _load_file(self, file):
        file_path = self._get_file_path(file)

        if os.path.exists(file_path):
            return open(file_path)
    
        return None

    def create_view(self, workflow_request : request, name : str, view_type : str, view_lambda : str, inputs : dict, props:dict):
        self.lambda_framework.log(f'create_view:name:{name}|view_type:{view_type}|view_lambda:{view_lambda}|inputs:{inputs}|props:{props}')

        if view_type == None:
            lambda_file = self._load_file(view_lambda)
            if lambda_file == None:
                return {'success': False, 'error_info': 'Lambda file not found'}

            result = self.vf_api.create_lambda_python(
                project=workflow_request.project_id, 
                type=self.vf_api.lambda_type.View,
                name=name, 
                fields={
                    'file_folder': workflow_request.version_folder_id,
                    'virtual': '1'
                },
                code=lambda_file.read())
            if not result.success:
                return {'success': False, 'error_info': result.error_info}
            view_type = result.id

        input_fields = {
                'file_folder' : workflow_request.version_folder_id,
                'view_type' : view_type,
                'virtual' : '1',
                'state' : 'COMPLETE',
                'color_legend_attribute' : '',
                'color_legend_attribute_index' : '-1',
                'color_legend_gradient' : 'isoluminant_cgo_70_c39_n256',
                'color_legend_interpolate_gradient' : '1',
                'color_legend_mode' : '2',
                'color_legend_range_max' : '100',
                'color_legend_range_min' : '0',
                'color_legend_range_step' : '1',
                'color_legend_reverse_gradient' : '0',
                'file_date' : str(1000 * int(time.time())),
                'file_type' : 'VIEW',
                'input_filter_colors' : '0',
                'input_filter_e' : '8',
                'input_filter_normals' : '0',
                'input_label_colors' : 'Use Ortho-imagery',
                'input_label_e' : 'Terrain',
                'input_label_normals' : 'Use high resolution detail',
                'input_type_colorlegend' : '7',
                'input_type_colors' : '6',
                'input_type_e' : '3',
                'input_type_normals' : '6',
                'input_value_colors' : '0',
                'input_value_normals' : '0',         
            }
            
        for key in inputs:
            input_fields['input_value_' + key] = inputs[key]

        for key in props:
            input_fields[key] = props[key]
            
        result = self.vf_api.create_entity_raw(
            project=workflow_request.project_id,
            type=self.vf_api.entity_type.View,
            name=name,
            fields=input_fields,
            crs={}
        )

        if not result.success:
            return {'success': False, 'error_info': result.error_info}
        view_object = result.id
        
        self.lambda_framework.log(f'created_view:name:{name}|view_object:{view_object}')

        result = self.vf_api.create_entity_raw(
            project=workflow_request.project_id,
            type=self.vf_api.entity_type.View,
            name=name,
            fields={
                'file_folder' : workflow_request.version_folder_id,
                'view_type' : 'container',
                'state' : 'COMPLETE',
                'entity_container' : view_object
            },
            crs={}
        )

        if not result.success:
            return {'success': False, 'error_info': result.error_info}
        return {'success': True, 'id': result.id, 'error_info': 'None'}

    def create_report(self, workflow_request : request, name : str, report_lambda : str, region : str, lod : int, inputs : dict, fields : dict = None, update_type : str = None):
        lambda_file = self._load_file(report_lambda)
        if lambda_file == None:
            return {'success': False, 'error_info': 'Lambda file not found'}
        
        result = self.vf_api.create_lambda_python(
            project=workflow_request.project_id, 
            type=self.vf_api.lambda_type.Report,
            name=f"Lambda for: {name}", 
            fields={
                'virtual': '1',
                'file_folder': workflow_request.version_folder_id
            },
            code=lambda_file.read())
        
        if not result.success:
            return {'success': False, 'error_info': result.error_info}
        
        report_lambda_id = result.id

        if fields == None:
            fields = {}

        fields['file_folder'] = workflow_request.version_folder_id

        if update_type:
            fields['callback_update_type'] = workflow_request.get_callback(update_type)

        result = self.vf_api.create_report(
            project=workflow_request.project_id, 
            program=report_lambda_id, 
            region=region,
            lod=str(lod),
            name=name, 
            fields=fields,
            inputs=inputs)
        
        if not result.success:
            return {'success': False, 'lambda_id': report_lambda_id, 'error_info': result.error_info}
        
        return {'success': True, 'id': result.id, 'lambda_id': report_lambda_id, 'error_info': 'None'}

    def create_lambda(self, workflow_request : request, name : str, type : str, lambda_code : str):
        lambda_file = self._load_file(lambda_code)
        if lambda_file == None:
            return {'success': False, 'error_info': 'Lambda file not found'}

        result = self.vf_api.create_lambda_python(
            project=workflow_request.project_id, 
            type=type,
            name=name, 
            fields={
                'file_folder': workflow_request.version_folder_id
            },
            code=lambda_file.read())
        
        if not result.success:
            return {'success': False, 'error_info': result.error_info}
        
        report_lambda_id = result.id
        return {'success': True, 'id': report_lambda_id}

    def create_export(self, workflow_request : request, name : str, export_lambda : str, region : str, lod : int, inputs : dict, fields : dict = None, update_type : str = None):
        lambda_file = self._load_file(export_lambda)
        if lambda_file == None:
            return {'success': False, 'error_info': 'Lambda file not found'}

        result = self.vf_api.create_lambda_python(
            project=workflow_request.project_id, 
            type=self.vf_api.lambda_type.Report,
            name="Export Lambda for " + name, 
            fields={
                'virtual': '1',
                'file_folder': workflow_request.version_folder_id
            },
            code=lambda_file.read())
        if not result.success:
            return {'success': False, 'error_info': result.error_info}
        report_lambda_id = result.id

        if fields == None:
            fields = {}

        fields['file_folder'] = workflow_request.version_folder_id
        fields['export_type'] = 'mesh'

        if update_type:
            fields['callback_update_type'] = workflow_request.get_callback(update_type)

        result = self.vf_api.create_export(
            project=workflow_request.project_id, 
            program=report_lambda_id, 
            region=region,
            lod=str(lod),
            name=name, 
            fields=fields,
            inputs=inputs)

        if not result.success:
            return {'success': False, 'lambda_id': report_lambda_id, 'error_info': result.error_info}

        return {'success': True, 'id': result.id, 'lambda_id': report_lambda_id, 'error_info': 'None'}

    def get_meta_attributes(self, workflow_request : request, projectId:str):
        attribute_product = workflow_request.get_product_property('META_ATTR_BM', 'report_entity')
        self.lambda_framework.log(f'attribute_product:{attribute_product}')
        file_name = 'report.csv'
        local_attr_file = os.path.join(workflow_request.scrap_folder, file_name)
        self.lambda_framework.log(f'Downloading {file_name} to {local_attr_file}...')
        if not self.vf_api.download_file(projectId, attribute_product, file_name, local_attr_file):
            return {'success': False, 'error_info': f'Could not download {file_name} to {local_attr_file}'}
        self.lambda_framework.log(f'Downloaded {file_name} to {local_attr_file}...')
        
        self.lambda_framework.log(f'Processing {local_attr_file}...')
        
        csvfile = open(f"{local_attr_file}", mode='r', encoding='utf-8-sig' )
        reader = csv.DictReader(csvfile)
        record_count = 0
        view_attribute = ''
        attributes_arr = []
        groups_arr = []
        grades_arr = []
        for row in reader:
            #self.lambda_framework.log(f'row:{row}')
            ID = row['Property']
            Report = row['Report']
            View = row['View']
            Group = row['Group']
            Grade = row['Grade']
            if View == '1' and view_attribute == '':
                self.lambda_framework.log(f'Assigning attribute: {ID} with index: {record_count}')
                view_attribute = ID
            if Report == '1':
                attributes_arr.append(ID)
            if Group == '1':
                groups_arr.append(ID)
            if Grade == '1':
                grades_arr.append(ID)
            record_count += 1

        attributes = ",".join(attributes_arr)
        groups = ",".join(groups_arr)
        grades = ",".join(grades_arr)

        self.lambda_framework.log(f'attributes:{attributes}')
        self.lambda_framework.log(f'groups:{groups}')
        self.lambda_framework.log(f'grades:{grades}') 

        return {'attributes':attributes, 'groups': groups, 'grades':grades, 'view_attribute': view_attribute}
        
    def notify_users(self, file_entity_id):
        self.lambda_framework.log(f'notify_users for file_entity_id: {file_entity_id}')
        file_entity = self.lambda_framework.get_entity(file_entity_id)
        if file_entity != None:
            emails_to = self.lambda_framework.get_notify_emails()
            if emails_to is None:
                self.lambda_framework.log('No email were sent because OS getenv variable vf_notify_emails is None')
                return { "success": True }
            
            self.lambda_framework.log(f'emails_to: {emails_to}')

            emails_to = emails_to.split(",")
            folder_entity = self.lambda_framework.get_entity(file_entity['file_folder'])
            parent_entity = self.lambda_framework.get_entity(folder_entity['file_folder'])
            
            if 'user' in file_entity and file_entity['user'] not in emails_to:
                emails_to.append(file_entity['user'])
            if 'user' in folder_entity and folder_entity['user'] not in emails_to:
                emails_to.append(folder_entity['user'])
            if 'user' in parent_entity and parent_entity['user'] not in emails_to:
                emails_to.append(parent_entity['user'])

            self.lambda_framework.log(f'notify users: {emails_to}')

            url = self.lambda_framework.get_notify_users_url()
            self.lambda_framework.log(f'notify url: {url}')

            if file_entity["state"] == "COMPLETE":
                subject = f"Completed {file_entity['name']} in {parent_entity['name']} ({folder_entity['name']})"
                body = f"Dear team member,\n\nThe following item has been completed:\n\n    {file_entity['name']} in {parent_entity['name']} ({folder_entity['name']})\n\nYou can access this item here:\n\n{self.lambda_framework.get_workflow_api()}app/catalog/{file_entity_id}\n\nPlease do not reply to this message. It has been generated by an automated workflow."
            else:
                subject = f"Error in {file_entity['name']} in {parent_entity['name']} ({folder_entity['name']})"
                body = f"Dear team member,\n\nWe have encountered some issues while processing the following item:    \n\n{file_entity['name']} in {parent_entity['name']} ({folder_entity['name']})\n\n For more information, please access the log tab of the item. You can access this item here:\n\n{self.lambda_framework.get_workflow_api()}app/catalog/{file_entity_id}\n\nPlease do not reply to this message. It has been generated by an automated workflow."

            self.lambda_framework.log(f'subject: {subject}')
            self.lambda_framework.log(f'body: {body}')

            data = {
                "from": "noreply@voxelfarm.com",
                "to": ",".join(emails_to),
                "subject": subject,
                "body": body
            }
            headers = {"Content-type": "application/json", "Accept": "text/plain"}

            req = requests.post(url, data=json.dumps(data), headers=headers)
            if req.status_code >= 200 and req.status_code < 300:
                self.lambda_framework.log(f'Emails sent successfully')
                return { "success": True }
            else:
                self.lambda_framework.log(f'Error sending the emails')
                return { "success": False }
        else:
            self.lambda_framework.log(f'Entity : {file_entity_id} not found')
            return { "success": False }

    def process_entity(self, workflow_request, type, name, fields = None, update_type = None):

        if fields == None:
            fields = {}

        fields['file_folder'] = workflow_request.version_folder_id

        if update_type:
            fields['callback_update_type'] = workflow_request.get_callback(update_type)

        api_result = self.vf_api.create_entity_processed(
            project=workflow_request.project_id, 
            type=type, 
            name=name, 
            fields=fields, 
            crs=workflow_request.crs, 
            callback=None)
        
        if update_type and api_result.success:
            self.increment_counter(update_type)
        
        return api_result

    def process_lambda_entity(self, workflow_request, name, inputs, code, files, fields = None, update_type = None):
        verified_files = []
        if files:
            for file in files:
                verified_files.append(self._get_file_path(file))

        if fields == None:
            fields = {}

        fields['file_folder'] = workflow_request.version_folder_id

        if update_type:
            fields['callback_update_type'] = workflow_request.get_callback(update_type)

        api_result =  self.vf_api.create_python_process_entity(
            project=workflow_request.project_id, 
            name=name, 
            fields=fields, 
            inputs=inputs,
            code=code,
            type='PROCESS',
            files=verified_files, 
            callback=None)
    
        if update_type and api_result.success:
            self.increment_counter(update_type)

        return api_result    





