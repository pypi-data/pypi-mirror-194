import mip as mip_interface
import itertools as it

sets = it.product

BINARY = mip_interface.BINARY
POSITIVE = mip_interface.CONTINUOUS
INTEGER = mip_interface.INTEGER
FREE = mip_interface.CONTINUOUS

def generate_variable(modelobject, var_type, var_name, b, dim=0):

    match var_type:

        case 'pvar':

            '''

            Positive Variable Generator


            '''

            if dim == 0:
                GeneratedVariable =  modelobject.add_var(var_type=POSITIVE)
            else:
                if len(dim) == 1:
                    GeneratedVariable =  {key: modelobject.add_var(var_type=POSITIVE) for key in dim[0]}
                else:
                    GeneratedVariable =  {key: modelobject.add_var(var_type=POSITIVE) for key in it.product(*dim)}
                            
        case 'bvar':

            '''

            Binary Variable Generator


            '''

            if dim == 0:
                GeneratedVariable =  modelobject.add_var(var_type=BINARY)
            else:
                if len(dim) == 1:
                    GeneratedVariable =  {key: modelobject.add_var(var_type=BINARY) for key in dim[0]}
                else:
                    GeneratedVariable =  {key: modelobject.add_var(var_type=BINARY) for key in it.product(*dim)}
      
                    
        case 'ivar':

            '''

            Integer Variable Generator


            '''

            if dim == 0:
                GeneratedVariable =  modelobject.add_var(var_type=INTEGER)
            else:
                if len(dim) == 1:
                    GeneratedVariable =  {key: modelobject.add_var(var_type=INTEGER) for key in dim[0]}
                else:
                    GeneratedVariable =  {key: modelobject.add_var(var_type=INTEGER) for key in it.product(*dim)}

                            
        case 'fvar':

            '''

            Free Variable Generator


            '''
            if dim == 0:
                GeneratedVariable =  modelobject.add_var(var_type=POSITIVE)
            else:
                if len(dim) == 1:
                    GeneratedVariable =  {key: modelobject.add_var(var_type=POSITIVE) for key in dim[0]}
                else:
                    GeneratedVariable =  {key: modelobject.add_var(var_type=POSITIVE) for key in it.product(*dim)}



    
    return  GeneratedVariable
    
