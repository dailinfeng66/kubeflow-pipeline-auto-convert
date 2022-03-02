import kfp
from kfp.v2 import dsl
from kfp.v2.dsl import component
from kfp.v2.dsl import component, Input, Output, OutputPath, Dataset, Model,InputPath
import kfp.components as comp
add=comp.load_component_from_url('http://10.23.71.70/kubeflow/pipeline/addcomponent.yml')
sub=comp.load_component_from_url('http://10.23.71.70/kubeflow/pipeline/subcomponent.yml')
@dsl.pipeline(name='simplepipeline',description='it's my first test to build a pipeline')
def firstpipeline(a:int=10,b:int=10,):
    a_bcc__b_fdfec=add(a=a,b=b,)
    fcf_fba_c_ac_aedff=add(a=a_bcc__b_fdfec.output,b=a_bcc__b_fdfec.output,)
    dac_cd_d_a_dbcbe=add(a=a_bcc__b_fdfec.output,b=fcf_fba_c_ac_aedff.output,)
    edcfde_f_c_db_ebecb=add(a=fcf_fba_c_ac_aedff.output,b=a_bcc__b_fdfec.output,)
    faa_dd_a_aa_adfcccd=sub(a=edcfde_f_c_db_ebecb.output,b=fcf_fba_c_ac_aedff.output,)
