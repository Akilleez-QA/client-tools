"""Pure Python receipt controls; synthetic PE headers are never executed."""
from pathlib import Path
import copy
import json
import struct
import tempfile
import unittest
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from receipt import ReceiptError, digest, verify_pair

class ReceiptTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        self.host=self.root/'host.exe';self.controller=self.root/'controller.exe'
        for path,architecture in [(self.host,0x14c),(self.controller,0x8664)]:
            data=bytearray(80);data[:2]=b'MZ';struct.pack_into('<I',data,60,64);data[64:68]=b'PE\0\0';struct.pack_into('<H',data,68,architecture);path.write_bytes(data)
        inputs={'sources':{'frozen.cpp':'a'*64},'headers':{'frozen.h':'b'*64},'tools':{'cl.exe':'c'*64},'libraries':{}}
        self.data={'schema':'miles-build-receipt-v4','stable_matrix':True,'builder_before':{'b':'x'},'builder_after':{'b':'x'},'source_snapshot_before':inputs['sources'],'source_snapshot_after':inputs['sources'],'builds':[]}
        for arch,path,machine in [('x86',self.host,0x14c),('amd64',self.controller,0x8664)]:
            self.data['builds'].append({'config':'Debug','architecture':arch,'exit_code':0,'inputs_unchanged':True,'before':copy.deepcopy(inputs),'after':copy.deepcopy(inputs),'output':{'sha256':digest(path),'machine':machine}})
        self.receipt=self.root/'receipt.json';self.write()
    def tearDown(self):self.temp.cleanup()
    def write(self):self.receipt.write_text(json.dumps(self.data));self.pin=digest(self.receipt)
    def verify(self):return verify_pair(self.receipt,self.pin,'Debug',self.host,self.controller)
    def test_valid_staged_outputs(self):self.assertEqual(len(self.verify()['outputs']),2)
    def test_changed_receipt_rejects_external_pin(self):self.receipt.write_text(self.receipt.read_text()+' ');self.assertRaises(ReceiptError,self.verify)
    def test_changed_host_rejected(self):self.host.write_bytes(self.host.read_bytes()+b'x');self.assertRaises(ReceiptError,self.verify)
    def test_changed_controller_rejected(self):self.controller.write_bytes(self.controller.read_bytes()+b'x');self.assertRaises(ReceiptError,self.verify)
    def test_missing_host_rejected(self):self.host.unlink();self.assertRaises(ReceiptError,self.verify)
    def test_missing_controller_rejected(self):self.controller.unlink();self.assertRaises(ReceiptError,self.verify)
    def test_wrong_architecture_rejected(self):self.controller.write_bytes(self.host.read_bytes());self.data['builds'][1]['output']['sha256']=digest(self.controller);self.write();self.assertRaises(ReceiptError,self.verify)
    def test_duplicate_identity_rejected(self):self.data['builds'].append(copy.deepcopy(self.data['builds'][0]));self.write();self.assertRaises(ReceiptError,self.verify)
    def test_failed_compile_rejected(self):self.data['builds'][0]['exit_code']=2;self.write();self.assertRaises(ReceiptError,self.verify)
    def test_changed_input_during_build_rejected(self):self.data['builds'][0]['after']['headers']['frozen.h']='z'*64;self.write();self.assertRaises(ReceiptError,self.verify)
    def test_missing_header_provenance_rejected(self):self.data['builds'][0]['before']['headers']={};self.data['builds'][0]['after']['headers']={};self.write();self.assertRaises(ReceiptError,self.verify)
    def test_mutable_current_source_cannot_change_provenance(self):
        (self.root/'frozen.cpp').write_text('changed after build');self.assertEqual(self.verify()['input_provenance'],'frozen build receipt; no post-run source hashing')
    def test_changed_builder_rejected(self):self.data['builder_after']['b']='other';self.write();self.assertRaises(ReceiptError,self.verify)
    def test_missing_configuration_rejected(self):self.assertRaises(ReceiptError,verify_pair,self.receipt,self.pin,'Release',self.host,self.controller)

if __name__=='__main__':unittest.main(verbosity=2)
