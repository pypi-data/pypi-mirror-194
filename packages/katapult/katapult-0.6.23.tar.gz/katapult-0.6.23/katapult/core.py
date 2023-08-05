from enum import IntFlag
from abc import ABC , abstractmethod
import katapult.utils as katapultutils
import json
import copy
import os
import re
import ntpath , posixpath
from katapult.attrs import *

kt_keypairName         = 'katapult-keypair'
kt_secGroupName        = 'katapult-sec-group-allow-ssh'
kt_secGroupNameMaestro = 'katapult-sec-group-allow-maestro'
kt_bucketName          = 'katapult-bucket'
kt_vpcName             = 'katapult-vpc'
kt_instanceNameRoot    = 'katapult-instance'
kt_instanceMaestro     = 'katapult-maestro'
kt_environmentNameRoot = 'katapult-env'
kt_maestroProfileName  = 'katapult-maestro-profile'
kt_maestroRoleName     = 'katapult-maestro-role'
kt_maestroPolicyName   = 'katapult-maestro-policy'

# NEW > STARTED > ASSIGNED > DEPLOYED > ( RUNNING | WATCHING <-> IDLE )

class KatapultProviderState(IntFlag):
    NEW           = 0  # provider created
    STARTED       = 1  # provider started
    ASSIGNED      = 2  # provider assigned jobs
    DEPLOYED      = 4  # provider deployed  
    RUNNING       = 8  # provider ran jobs
    WATCHING      = 16 # provider is watching jobs
    IDLE          = 32 # provider has stopped running jobs and watching
    ANY           = 32 + 16 + 8 + 4 + 2 + 1     

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    CBLACK  = '\33[30m'
    CRED    = '\33[31m'
    CGREEN  = '\33[32m'
    CYELLOW = '\33[33m'
    CBLUE   = '\33[34m'
    CVIOLET = '\33[35m'
    CBEIGE  = '\33[36m'
    CWHITE  = '\33[37m'

    CBLACKBG  = '\33[40m'
    CREDBG    = '\33[41m'
    CGREENBG  = '\33[42m'
    CYELLOWBG = '\33[43m'
    CBLUEBG   = '\33[44m'
    CVIOLETBG = '\33[45m'
    CBEIGEBG  = '\33[46m'
    CWHITEBG  = '\33[47m'        

class KatapultError(Exception):
    pass

class KatapultInstanceState(IntFlag):
    UNKNOWN     = 0
    STARTING    = 1  # instance starting
    RUNNING     = 2  # instance running
    STOPPING    = 4  # stopping
    STOPPED     = 8  # stopped
    TERMINATING = 16 # terminating
    TERMINATED  = 32 # terminated
    ANY         = 32 + 16 + 8 + 4 + 2 + 1     


class KatapultProcessState(IntFlag):
#    FOO = 100
    CREATED   = 0  # when created
    WAIT      = 1  # waiting for bootstraping
    QUEUE     = 2  # queued (for sequential scripts)
    IDLE      = 4  # script about to start
    RUNNING   = 8  # script running
    DONE      = 16 # script has completed
    ABORTED   = 32 # script has been aborted
    UNKNOWN   = 64 # set != 0 otherwise it may test positive when watching
    ANY       = 64 + 32 + 16 + 8 + 4 + 2 + 1 

class KatapultPlatform(IntFlag):
    UNKNOWN     = 0
    LINUX       = 1
    WINDOWS     = 2
    WINDOWS_WSL = 3
    MOCK        = 4 # instance = local machine (for mocking/testing)

class KatapultInstance():

    def __init__(self,config,id,proprietaryData=None):
        # instance region
        self._region   = config.get('region')
        # naming
        self._name     = init_instance_name(config)
        self._id       = id
        self._rank     = config.get('rank',"1.1")
        # IP / DNS
        self._ip_addr  = None
        self._dns_addr = None
        self._ip_addr_priv = None
        self._dns_addr_priv = None
        # state
        self._state    = KatapultProcessState.CREATED
        # the config the instance has been created on
        self._config   = config 
        # dict data associated with it (AWS response data e.g.)
        self._data     = proprietaryData
        # jobs list
        self._jobs     = [ ]
        # env dict
        self._envs     = dict()
        # invalid
        self._invalid  = False
        self._platform = KatapultPlatform.UNKNOWN
        self._reachability = False

    def get_region(self):
        return self._region

    def get_id(self):
        return self._id 
     
    def get_name(self):
        return self._name

    def get_rank(self):
        return self._rank

    def get_ip_addr(self):
        return self._ip_addr

    def get_dns_addr(self):
        return self._dns_addr 

    def get_ip_addr_priv(self):
        return self._ip_addr_priv

    def get_dns_addr_priv(self):
        return self._dns_addr_priv

    def get_reachability(self):
        return self._reachability

    def get_cpus(self):
        return self._config.get('cpus')

    def get_state(self):
        return self._state

    def get_platform(self):
        return self._platform

    def get_active_processes(self):
        processes_res = []
        for job in self._jobs:
            dpl_jobs = job.get_deployed_jobs()
            for dpl_job in dpl_jobs:
                for process in dpl_job.get_processes():
                    if process.is_active():
                        processes_res.append(process)
        return processes_res

    def get_home_dir(self,absolute=True):
        if self._platform == KatapultPlatform.LINUX or self._platform == KatapultPlatform.WINDOWS_WSL:
            return '/home/' + self.get_config('img_username') if absolute else '%HOME'
        elif self._platform == KatapultPlatform.WINDOWS:
            return 'C:\>' + self.get_config('img_username') if absolute else '%HOME%'
        elif self._platform == KatapultPlatform.UNKNOWN: 
            return os.path.expanduser( '~' )
        elif self._platform == KatapultPlatform.MOCK: # those are local instances (used by Mock/Testing)
            return os.path.join( os.getcwd() , 'tests_tmp' , 'instances' , self.get_name() )

    def get_global_dir(self):
        return self.path_join( self.get_home_dir() , 'run' )

    def path(self):
        if self._platform == KatapultPlatform.LINUX or self._platform == KatapultPlatform.WINDOWS_WSL:
            return posixpath
        elif self._platform == KatapultPlatform.WINDOWS:
            return ntpath
        elif self._platform == KatapultPlatform.UNKNOWN:
            return os.path
        elif self._platform == KatapultPlatform.MOCK:
            return os.path

    def path_join(self,*args):
        return self.path().join(*args)
    
    def path_dirname(self,path):
        return self.path().dirname(path)
    
    def path_basename(self,path):
        return self.path().basename(path)
    
    def path_sep(self):
        return self.path().sep

    # def path_join(self,*args):
    #     sep = self.path_sep()
    #     first = True
    #     fargs = []
    #     for arg in args:
    #         fargs.append( arg.rstrip(sep) if first else arg.strip(sep) )
    #     return sep.join(fargs)

    # def path_dirname(self,path):
    #     #return os.path.dirname(path)
    #     sep = self.path_sep()
    #     path_expl = path.split(sep)
    #     if len(path_expl)>2:
    #         return sep.join( path_expl[:-1] )
    #     else:
    #         return ''
    
    # def path_basename(self,path):
    #     #return os.path.basename(path)
    #     sep = self.path_sep()
    #     path_expl = path.split(sep)
    #     if len(path_expl)>1:
    #         return path_expl[-1]
    #     else:
    #         return ''


    # def path_sep(self):
    #     if self._platform == KatapultPlatform.LINUX or self._platform == KatapultPlatform.WINDOWS_WSL:
    #         return '/'
    #     elif self._platform == KatapultPlatform.WINDOWS:
    #         return '\\'

    def set_ip_addr(self,value):
        self._ip_addr = value

    def set_ip_addr_priv(self,value):
        self._ip_addr_priv = value

    def set_dns_addr(self,value):
        self._dns_addr = value
     
    def set_dns_addr_priv(self,value):
        self._dns_addr_priv = value

    def set_state(self,value):
        self._state = value 

    def set_reachability(self,value):
        self._reachability = value

    def set_platform(self,value):
        self._platform = value 

    def set_invalid(self,val):
        self._invalid = val

    def set_data(self,data):
        self._data = data 
    
    def get_data(self,key):
        if not self._data:
            return None
        return self._data.get(key,None)
     
    def get_config(self,key):
        if not self._config:
            return None
        return self._config.get(key,None)

    def reset_jobs(self):
        self._jobs = []
    
    def reset_envs(self):
        self._envs = dict()

    def append_job(self,job):
        for j in self._jobs:
            if j == job:
                debug(1,"job already added to instance",job,color=bcolors.WARNING)
                return
        self._jobs.append(job)
        env = job.get_env()
        self._envs[env.get_name()] = env 

    def get_environments(self):
        return self._envs.values()

    def get_jobs(self):
        return self._jobs

    def get_active_processes(self):
        processes_res = []
        for job in self._jobs:
            for p in job.get_active_processes():
                processes_res.append(p)
        return processes_res

    def get_config_DIRTY(self):
        return self._config

    def is_invalid(self):
        return self._invalid

    def update_from_instance(self,instance):
        self._region   = instance._region
        self._name     = instance._name
        self._id       = instance._id 
        self._rank     = instance._rank
        self._ip_addr  = instance._ip_addr
        self._dns_addr = instance._dns_addr
        self._ip_addr_priv  = instance._ip_addr_priv
        self._dns_addr_priv = instance._dns_addr_priv
        self._state    = instance._state
        self._reachability  = instance._reachability
        self._platform = instance._platform
        self._config   = instance._config #copy.deepcopy(instance._config)
        self._data     = copy.deepcopy(instance._data)        

    def __repr__(self):
        # return "{0}: REGION = {1} , ID = {2} , NAME = {3} , IP = {4} , CPUS = {5} , RANK = {6}".format(type(self).__name__,self._region,self._id,self._name,self._ip_addr,self.get_cpus(),self._rank)
        # return "{0}: ID = {1} , NAME = {2} , IP = {3} , CPUS = {4}".format(type(self).__name__,self._id,self._name,self._ip_addr,self.get_cpus())
        return "{0}: NAME = {1} , IP = {2}".format(type(self).__name__,self._name,self._ip_addr)

    def __str__(self):
        # return "{0}: REGION = {1} , ID = {2} , NAME = {3} , IP = {4} , CPUS = {5} , RANK = {6}".format(type(self).__name__,self._region,self._id,self._name,self._ip_addr,self.get_cpus(),self._rank)
        # return "{0}: ID = {1} , NAME = {2} , IP = {3} , CPUS = {4}".format(type(self).__name__,self._id,self._name,self._ip_addr,self.get_cpus())
        return "{0}: NAME = {1} , IP = {2}".format(type(self).__name__,self._name,self._ip_addr)

class KatapultInstanceProxy(KatapultInstance):

    def __init__(self,name,config=None):
        self._name = name
        self._config = config


class KatapultEnvironment():

    def __init__(self,projectName,env_config):
        self._config   = env_config
        self._project  = projectName
        _env_obj       = katapultutils.compute_environment_object(env_config)
        self._hash     = katapultutils.compute_environment_hash(_env_obj)
        if not self._config.get('name'):
            self._name = kt_environmentNameRoot

            append_str = '-' + self._hash
            if env_config.get('dev',False) == True:
                append_str = ''
            if projectName:
                self._name = kt_environmentNameRoot + '-' + projectName + append_str
            else:
                self._name = kt_environmentNameRoot + append_str
        else:
            self._name = self._config.get('name')

    def get_name(self):
        return self._name

    def get_name_with_hash(self):
        return self._name + '-' + self._hash

    def get_config(self,key):
        return self._config.get(key)

    def get_config_DIRTY(self):
        return self._config

    def get_env_obj(self):
        _env_obj = katapultutils.compute_environment_object(self._config)
        return _env_obj 

    def get_hash(self):
        return self._hash

    def json(self):
        return json.dumps(self.get_env_obj())          

    def deploy(self,instance):
        return KatapultDeployedEnvironment(self,instance)

    def __repr__(self):
        return "{0}: NAME = {1} , HASH = {2}".format(type(self).__name__,self._name,self._hash)

    def __str__(self):
        return "{0}: NAME = {1} , HASH = {2}".format(type(self).__name__,self._name,self._hash)

class KatapultEnvironmentProxy(KatapultEnvironment):

    def __init__(self,hash,config=None):
        self._hash = hash
        self._config = config


# "Temporary" objects used when starting scripts      

class KatapultDeployedEnvironment(KatapultEnvironment):

    # constructor by copy...
    def __init__(self, env, instance):
        #super().__init__( env._project , env._config )
        self._config   = env._config #copy.deepcopy(env._config)
        self._project  = env._project
        self._hash     = env._hash
        self._name     = env._name
        self._instance = instance
        self._path     = instance.path_join( instance.get_home_dir() , 'run' , self.get_name_with_hash())

    def get_path(self):
        return self._path

    def get_instance(self):
        return self._instance

    def json(self):
        _env_obj = super().get_env_obj()
        # overwrite name in conda config as well
        if _env_obj['env_conda'] is not None:
           _env_obj['env_conda']['name'] = self.get_name_with_hash()
        _env_obj['name'] = self.get_name_with_hash()
        # replace __REQUIREMENTS_TXT_LINK__ with the actual requirements.txt path (dependent of config and env hash)
        # the file needs to be absolute
        requirements_txt_path = self._instance.path_join(self._path,'requirements.txt')
        _env_obj = katapultutils.update_requirements_path(_env_obj,requirements_txt_path)
        return json.dumps(_env_obj)  


class KatapultJob():

    def __init__(self,job_cfg,rank):
        self._config    = job_cfg
        self._rank      = rank
        self._hash      = katapultutils.compute_job_hash(self._config)
        self._id        = katapultutils.generate_unique_id() + '_' + str(rank)
        self._env       = None
        self._instance  = None
        self._deployed = [ ]
        if not 'input_files' in self._config:
            print("\033[20minput name missing for Job\033[0m",self)
        if not 'output_files' in self._config:
            print("\033[91mConfiguration requires an output file name\033[0m",self)
            raise KatapultError() 

    def attach_env(self,env):
        self._env = env 
        self._config['env_name'] = env.get_name()

    def get_hash(self):
        return self._hash

    def get_id(self):
        return self._id

    def get_config(self,key,defaultVal=None):
        return self._config.get(key,defaultVal)

    def get_config_DIRTY(self):
        return self._config

    def get_env(self):
        return self._env

    def get_instance(self):
        return self._instance

    def get_rank(self):
        return self._rank

    def get_deployed_jobs(self):
        return self._deployed

    def get_deployed_job(self,instance):
        for dpl_job in self._deployed:
            if dpl_job.get_instance() == instance:
                return dpl_job
        return None

    def deploy(self,dpl_env,add_permanently=True):
        # instance = dpl_env.get_instance()
        # dpl_job  = self.get_deployed_job(instance)
        # if dpl_job:
        #     return dpl_job
        dpl_job  = KatapultDeployedJob(self,dpl_env)
        if add_permanently:
            self._deployed.append(dpl_job)
        return dpl_job

    def has_completed(self):
        for dpl_job in self._deployed:
            for process in dpl_job.get_processes():
                if process.get_state() == KatapultProcessState.DONE:
                    return True
        return False

    def has_processes(self):
        for dpl_job in self._deployed:
            for process in dpl_job.get_processes():
                return True
        return False

    def get_last_process(self):
        if not self._deployed or len(self._deployed)==0:
            return None
        # last_dpl_job = self._deployed[len(self._deployed)-1]
        # processes = last_dpl_job.get_processes()
        # if not processes or len(processes)==0:
        #     return None 
        # return processes[len(processes)-1]
        last_process = None
        count = 0 
        for dpl_job in self._deployed:
            for process in dpl_job.get_processes():
                last_process = process
                count = count + 1
        return last_process

    # def get_active_processes(self):
    #     processes_res = []
    #     for dpl_job in self._deployed:
    #         for p in dpl_job.get_active_processes():
    #             processes_res.append(p)
    #     return processes_res

    def get_active_processes(self):
        if not self._deployed or len(self._deployed)==0:
            return []
        res = []
        for dpl_job in self._deployed:
            for process in dpl_job.get_active_processes():
                res.append(process)
        return res

    def set_instance(self,instance):
        self._instance = instance
        instance.append_job(self)

    def str_simple(self):
        return "{0}: ID = {1} , HASH = {2} , ENV = {3}: {4}".format(type(self).__name__,self.get_id(),self.get_hash(),self.get_env().get_name() if self.get_env() else None,self.get_config('run_script') or self.get_config('run_command') )

    def __repr__(self):
        return "{0}: ID = {1} , HASH = {2} , INSTANCE = {3} , ENV = {4}".format(type(self).__name__,self.get_id(),self.get_hash(),self.get_instance(),self.get_env().get_name() if self.get_env() else None)
         
    def __str__(self):
        return "{0}: ID = {1} , HASH = {2} , INSTANCE = {3} , ENV = {4}".format(type(self).__name__,self.get_id(),self.get_hash(),self.get_instance(),self.get_env().get_name() if self.get_env() else None)


class KatapultJobProxy(KatapultJob):

    def __init__(self,id,config=None):
        self._id     = id 
        self._rank   = int( re.sub(r'[0-9a-zA-Z]+_','',self._id) )
        self._config = config


# "Temporary" objects used when starting scripts     
# "Proxy" class that keeps the link with "copied" object
# We proxy all parent methods instead of using inheritance
# this allows to keep the same behavior while keeping the link and sharing memory objects

class KatapultDeployedJob(KatapultJob):

    def __init__(self,job,dpl_env):
        #super().__init__( job._config )
        self._job       = job
        #self._config    = copy.deepcopy(job._config)
        #self._hash      = job._hash
        #self._instance  = job._instance
        self._processes = []
        self._env       = dpl_env
        self._instance  = dpl_env.get_instance()
        self._path      = self._instance.path_join( dpl_env.get_path() , self.get_hash() )
        self._command   = katapultutils.compute_job_command(self._instance,self._path,self._job._config)

    def attach_process(self,process):
        self._processes.append(process)

    def get_path(self):
        return self._path

    def get_command(self):
        return self._command

    def attach_env(self,env):
        raise KatapultError('Can not attach env to deployed job')

    # proxied
    def get_rank(self):
        return self._job._rank

    # proxied
    def get_hash(self):
        return self._job._hash

    # proxied
    def get_id(self):
        return self._job._id

    # proxied
    def get_config(self,key,defaultVal=None):
        return self._job._config.get(key,defaultVal)

    # proxied
    def get_config_DIRTY(self):
        return self._job.get_config_DIRTY()

    def get_env(self):
        return self._env

    def get_instance(self):
        return self._instance   

    def get_processes(self):
        return self._processes

    def get_active_processes(self):
        processes_res = []
        for p in self._processes:
            if p.is_active():
                processes_res.append(p)
        return processes_res

    def deploy(self,dpl_env):
        raise KatapultError('Can not deploy a deployed job')

    def set_instance(self,instance):
        raise KatapultError('Can not set the instance of a deployed job')


class KatapultProcess():

    def __init__(self,dpl_job,batch,pid=None):
        self._job   = dpl_job
        self._uid   = katapultutils.generate_unique_id() 
        self._pid   = pid
        self._pid_child    = None
        self._batch = batch
        self._state = KatapultProcessState.UNKNOWN
        self._active = True
        self._aborted_reason = None
        self._substate = None
        self._job.attach_process(self)
     
    def get_uid(self):
        return self._uid

    def get_pid(self):
        return self._pid

    def get_pid_child(self):
        return self._pid_child

    def get_batch(self):
        return self._batch 

    def deactivate(self):
        self._active = False

    def is_active(self):
        return self._active 

    def get_path(self):
        instance = self._job.get_instance()
        return instance.path_join( self._job.get_path() , self._uid )

    def get_state(self):
        return self._state

    def get_state_object(self,withJobRef=False,withJobCfg=False):
        obj = {
            'state' : self._state ,
            'substate' : self._substate ,
            'aborted_reason' : self._aborted_reason ,
            'uid' : self._uid 
        }
        if withJobRef:
            obj['job_id'] = self._job.get_id()
        if withJobCfg:
            obj['job_config'] = self._job.get_config_DIRTY()
        return obj
    
    def set_state(self,value):
        self._state = value

    def set_substate(self,substate):
        self._substate = substate

    def get_substate(self):
        return self._substate

    def set_aborted_reason(self,reason):
        self._aborted_reason = reason 

    def set_pid(self,value):
        self._pid = value 

    def set_pid_child(self,value):
        self._pid_child = value 

    def get_job(self):
        return self._job 

    def get_instance(self):
        return self._job.get_instance()

    def str_simple(self):
        if self._state != KatapultProcessState.DONE and self._state != KatapultProcessState.RUNNING:
            details = self._aborted_reason if self._aborted_reason else self._substate
        else:
            details = None

        if self._batch:
            if details:
                return "KatapultProcess: UID = {0} , PID = {1} , PID(child) = {2} , BATCH = {3} , STATE = {4} ({5})".format(self._uid,str(self._pid).rjust(5),str(self._pid_child).rjust(5),self._batch.get_uid(),self._state.name,details)
            else:
                return "KatapultProcess: UID = {0} , PID = {1} , PID(child) = {2} , BATCH = {3} , STATE = {4}".format(self._uid,str(self._pid).rjust(5),str(self._pid_child).rjust(5),self._batch.get_uid(),self._state.name)
        else:
            if details:
                return "KatapultProcess: UID = {0} , PID = {1} , PID(child) = {2} , STATE = {3} ({4})".format(self._uid,str(self._pid).rjust(5),str(self._pid_child).rjust(5),self._state.name,details)
            else:
                return "KatapultProcess: UID = {0} , PID = {1} , PID(child) = {2} , STATE = {3}".format(self._uid,str(self._pid).rjust(5),str(self._pid_child).rjust(5),self._state.name)

    def __repr__(self):
        if self._state != KatapultProcessState.DONE and self._state != KatapultProcessState.RUNNING:
            details = self._aborted_reason if self._aborted_reason else self._substate
        else:
            details = None
        if details:
            return "KatapultProcess: job = {0} , UID = {1} , PID = {2} , PID(child) = {3} , STATE = {4} ({5})".format(self._job,self._uid,str(self._pid).rjust(5),str(self._pid_child).rjust(5),self._state.name,details)
        else:
            return "KatapultProcess: job = {0} , UID = {1} , PID = {2} , PID(child) = {3} , STATE = {4}".format(self._job,self._uid,str(self._pid).rjust(5),str(self._pid_child).rjust(5),self._state.name)
         
    def __str__(self):
        return self.__repr__()

class KatapultRunSession():

    def __init__(self,number):
        self._number  = number 
        self._id      = katapultutils.generate_unique_id() + '_' + str(number)
        self._batches = []

    def create_batch(self):
        batch = KatapultBatch(self)
        self._batches.append(batch)
        return batch

    def get_active_processes(self,instance=None):
        processes_res = []
        for batch in self._batches:
            for p in batch.get_active_processes(instance):
                processes_res.append(p)
        return processes_res

    def get_processes(self):
        processes_res = []
        for batch in self._batches:
            for p in batch.get_processes():
                processes_res.append(p)
        return processes_res        

    def get_number(self):
        return self._number

    def get_id(self):
        return self._id

    # return the processes that have been run for each job
    # (kinda last_processes but through a different view point)
    def get_ran_processes(self):
        processes = dict()
        # scan all the processes in order of the batches ...
        for batch in self._batches:
            for process in batch.get_processes():
                dpl_job = process.get_job()
                rank    = dpl_job.get_rank()
                processes[rank] = process # this will keep the last process ran for this job rank
        
        return processes.values()


    def deactivate(self,instance=None):
        for batch in self._batches:
            batch.deactivate_processes(instance)

    def mark_aborted(self,instance,state_mask,reason=None):
        for batch in self._batches:
            batch.mark_aborted(instance,state_mask,reason)

    # get the instances this RunSession has ran on
    def get_instances(self):
        instances = dict()
        # scan all the processes in order of the batches ...
        for batch in self._batches:
            for process in batch.get_processes():
                dpl_job  = process.get_job()
                instance = dpl_job.get_instance()
                instances[instance] = instance 
        
        return instances.values()

    def get_batch(self,identifier):
        for batch in self._batches:
            if batch.get_uid() == identifier:
                return batch
        return None

class KatapultRunSessionProxy(KatapultRunSession):

    def __init__(self,session_id):
        self._id     = session_id
        self._number = int( re.sub(r'[0-9a-zA-Z]+_','',self._id) )

class KatapultBatch():

    def __init__(self,run_session):
        self._uid      = katapultutils.generate_unique_id()
        self._session  = run_session
        self._instances_processes = dict()

    def get_uid(self):
        return self._uid

    def get_session(self):
        return self._session

    def create_process(self,dpl_job):
        process   = KatapultProcess( dpl_job , self )
        instance  = dpl_job.get_instance()
        inst_name = instance.get_name()
        if not inst_name in self._instances_processes:
            self._instances_processes[inst_name] = []
        self._instances_processes[inst_name].append(process)
        return process

    def get_processes(self):
        processes_res = []
        for instance_name , processes in self._instances_processes.items():
            for process in processes:
                processes_res.append(process)
        return processes_res

    def get_active_processes(self,instance=None):
        processes_res = []
        if instance:
            if instance.get_name() in self._instances_processes:
                for process in self._instances_processes[instance.get_name()]:
                    if process.is_active():
                        processes_res.append(process)
        else:
            for instance_name , processes in self._instances_processes.items():
                for process in processes:
                    if process.is_active():
                        processes_res.append(process)
        return processes_res

    def deactivate_processes(self,instance=None):
        for instance_name , processes in self._instances_processes.items():
            if not instance or instance.get_name() == instance_name:
                for process in processes:
                    process.deactivate()

    # mark the currently active process as ABORTED
    def mark_aborted(self,instance,state_mask,reason=None):
        for process in self.get_active_processes(instance):
            if process.get_state() & state_mask:
                process.set_state(KatapultProcessState.ABORTED)
                if reason:
                    process.set_aborted_reason(reason)

def init_instance_name(instance_config):
    
    if 'maestro' not in instance_config:

        if instance_config.get('dev',False)==True:
            append_str = '' 
        else:
            append_str = '-' + katapultutils.compute_instance_hash(instance_config)

        if 'rank' not in instance_config:
            debug(1,"\033[93mDeveloper: you need to set dynamically a 'rank' attribute in the config for the new instance\033[0m")
            sys.exit(300) # this is a developer error, this should never happen so we can use exit here
            
        if 'project' in instance_config:
            return kt_instanceNameRoot + '-' + instance_config['project'] + '-' + instance_config['rank'] + append_str
        else:
            return kt_instanceNameRoot + '-' + instance_config['rank'] + append_str
    
    else:

        # if 'project' in instance_config:
        #     return kt_instanceMaestro + '-' + instance_config['project'] 
        # else:
        #     return kt_instanceMaestro

        # ultimately, the maestro will be shared across projects... (to save $)
        if instance_config.get('_maestro_name_proj',False)==True:
            return kt_instanceMaestro + '-' + instance_config['project'] 
        else:
            return kt_instanceMaestro
