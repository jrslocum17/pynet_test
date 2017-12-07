from snmp_helper import snmp_get_oid, snmp_extract

class SNMP_Router(object):

    def __init__(self, router_info_dict):
        self.router = router_info_dict['router']
        self.router_info = (router_info_dict['ip_addr'], router_info_dict['community'],
                              router_info_dict['port'])

    def Get_OID(self,oid):
        '''
        Given an SNMP OID, return the value in ASCII text
        :param oid: The SNMP OID
        :return: The value of the SNMP data in ASCII
        '''
        snmp_data = snmp_get_oid(self.router_info, oid)
        return snmp_extract(snmp_data)

    def Get_Router_Info(self,oid_list):
        '''
        Given a list of SNMP OIDs as a dictionary, return router info as ASCII text
        :param oid: The SNMP OID
        :return: The router information as text
        '''
        output = ""
        for oid in oid_list:
            output += oid['OID_NAME'] + ": "
            output += self.Get_OID(oid['OID_VALUE']) + "\n"
        output += '\n'
        return output