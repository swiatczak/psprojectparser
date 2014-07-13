__author__="Janusz Swiatczak"
__date__ ="12/09/2012"
import re
import os

INSTANCE_START_TAG = re.compile(r'<INSTANCE CLASS="(.*)"', re.I)
INSTANCE_END_TAG = re.compile(r'</INSTANCE>', re.I)

PEOPLECODE_SECTION = 'PCM'

pathRule = lambda x: '.' if int(x) in (12,39) else ('' if not x or int(x) == 0 else os.sep)

PATH_KEYS = { 'PCM' : (('eObjectID_0', lambda x: '{}{}'.format(CLASSES[int(x)], os.sep)) , ('szObjectValue_0', str),
                       ('eObjectID_1', pathRule), ('szObjectValue_1', str),
                       ('eObjectID_2', pathRule), ('szObjectValue_2', str),
                       ('eObjectID_3', pathRule), ('szObjectValue_3', str),
                       ('eObjectID_4', pathRule), ('szObjectValue_4', str),
                       ('eObjectID_5', pathRule), ('szObjectValue_5', str),
                       ('eObjectID_6', pathRule), ('szObjectValue_6', str)),
              'SRM' : (('szSqlType', lambda x: '{}{}'.format(SQL_TYPES.get(x), os.sep)), ('szSqlId', lambda x: re.sub(r'\s+', '.', str(x))))
                       }

SQL_TYPES = {'0': 'SQL', '1': 'APP_ENGINE_SQL1', '2':'VIEWSQL', '6':'APP_ENGINE2' }

EXTENSIONS = {'PCM'    : {'ext': 'peoplecode', 'flds': ['peoplecode_text']} ,
              'SRM'    : {'ext': 'sql'       , 'flds': ['lpszSqlText'] }}

NAME_MAP = {'ACM'     : ['szActivityName'],
            'AEM'     : ['szApplId'] ,
            'AES'     : ['szApplId' , 'szSection'],
            'APM'     : ['szPackageId'],
            'BCM'     : ['szBcName'],
            'BMM'     : ['szAcemodelid'], # - PSACEMDLDEFN
            'BPM'     : ['szBusProcName'],
            'CDM'     : ['szColorName','szOprId'],
            'CRM'     : ['szContName','eContType','nAltContNum'],
            'CLM'     : ['szClassId'],
            'CQDM'    : ['szConqrsname'], # connected query ?
            'FDM'     : ['szFormatFamily'],
            'FRM'     : ['szFilerefname', 'szFilereftypecode'],
            'FIELD'   : ['szFieldName'],
            'FLM'     : ['szDefnName'], #File Layout - PSFLDDEFN
            'IOM'     : ['szIOName'],
            'MDM'     : ['szMenuName'],
            'MNDM'    : ['szMsgNodeName'],
            'MPM'     : ['szMobilePageName'],
            'MSDM'    : ['szMsgName','lVersion'],
            'OPRHM'   : ['szOperationname','szHandlername'],
            'OPRM'    : ['szOperationname','szDefaultversion'],
            'OPRVM'   : ['szOperationname','szDefaultversion'],
            'PBM'     : ['szPbmType'], #optimisation problem type - PSOPTPRBTYPE
            'PCM'     : ['eObjectID_0','szObjectValue_0','eObjectID_1','szObjectValue_1','eObjectID_2','szObjectValue_2','eObjectID_3','szObjectValue_3','eObjectID_4','szObjectValue_4','eObjectID_5','szObjectValue_5','eObjectID_6','szObjectValue_6'],
            'PDM'     : ['szPnlName'],
            'PGM'     : ['szPnlGrpName'],
            'PJM'     : ['szProjectName'],
            'PRDM'    : ['szPortalName'], # Portal Definition - PSPRDMDEFN
            'PRSM'    : ['szPortalName','cRefType','szObjName'],
            'PRSM844' : ['szPortalName','cRefType','szObjName'],
            'PSD'     : ['szPrcsType','szPrcsName'],
            'PSD844'  : ['szPrcsType','szPrcsName'],
            'PSJ'     : ['szJobName'], #Proc Job Def - PS_PRCSJOBDEFN
            'PSR'     : ['szRecurName'], #Recurrence - PS_PRCSRECUR
            'PSS'     : ['szServerName'],
            'PSS844'  : ['szServerName'],
            'PST'     : ['szPrcsType','szOpsys','szDbType'],
            'QDM'     : ['szOprId', 'szQryName'],
            'RCMTM'   : ['szPortalName', 'szPortalObjName'], #RC Menu ?
            'RCSCM'   : ['szPortalName', 'szPortalObjName', 'szServiceId', 'nInstanceId'], #RC Service content ?
            'RCSDM'   : ['szServiceId' , 'cServiceType'], #RC Service Definition
            'RDM'     : ['szRecName'],
            'RTDM'    : ['szRoutingdefnname'],
            'SCMA'    : ['szMsgname','szApmsgver'], #message schema
            'SCNFM'   : ['szPortalName', 'szPortalObjName', 'szServiceId'], #RC Service Configuration ?
            'SDM'     : ['szStyleName'], #StyleDefinition - PSSTYLEDEFN
            'SRM'     : ['szSqlId','szSqlType'], #AE SQL, Transform , etc. - PSAESTEPDEFN
            'SRVM'    : ['szIb_servicename'],
            'SSM'     : ['szStyleSheetName'], # StyleSheet Definition - PSSTYLSHEETDEFN
            'SUDM'    : ['szMsgName', 'szSubName'], # Message Subscription - PSSUBDEFN
            'TSM'     : ['szTreeStrctId'],
            'TYC'     : ['szFilereftypecode'],
            'URL'     : ['szUrlId'],
            'XTM'     : ['szFieldName'],
            'XTRDM'   : ['szTemplate_id'],
            'XRRDM'   : ['szReport_defn_id'],
            'FILEM'   : ['szFileId','szFileName'],
            'XPDSM'   : ['szDs_type', 'szDs_id'],
            'WSDL'    : ['szIb_wsdlname', 'nIb_wsdlversion'] # WSDL definition
            }

CLASSES =   [  'NONE', 'RECORD', 'FIELD', 'MENU', 'MENUBAR', 'MENUITEM', 'DBFIELD', 'BUSINESSPROCESS', 'BUSINESSPROCESSMAP',
               'PAGE', 'COMPONENT', 'PROJECT', 'METHOD', 'FUNCTION', 'SOURCETOKEN',
               'SOURCELINE', 'LANGUAGECODE', 'ACCESS_GROUP', 'ACTIVITYNAME', 'COLORNAME', 'DBTYPE',
               'EFFDT', 'FIELDVALUE', 'FORMATFAMILY', 'INDEXID', 'OPRID', 'OPSYS', 'PRCSJOBNAME',
               'PRCSNAME', 'PRCSTYPE', 'QRYNAME', 'RECURNAME', 'ROLENAME', 'SERVERNAME', 'SETID',
               'STYLENAME', 'TREE_NAME', 'TREE_STRCT_ID', 'LONG_NAME', 'MARKET', 'PAGEREF', 'COMPONENTREF',
               'SYSCOLOR', 'STYLE', 'FIELD_FORMAT', 'TOOLBAR', 'FILEREF', 'TABLESPACE', 'MESSAGE_SET_NBR',
               'MESSAGE_NBR', 'MESSAGE_DESCR', 'DIMENSION_ID', 'DIMENSION_TYPE', 'DIMENSION_DESCR',
               'ANALYSIS_MODEL_ID', 'ANALYSIS_MODEL_DESCR', 'ANALYSIS_DB_ID', 'CUBE_TEMPLATE_DESCR',
               'BUSINESSPROCESSREF', 'ACTIVITYREF', 'MESSAGE', 'CHANNEL', 'MESSAGE_NODE', 'DUMMY',
               'INTERFACE_OBJECT', 'SQL', 'AEAPPLICATIONID', 'PAGEFIELD', 'SETCNTRLVALUE', 'CLASS_OLDBUSPROC',
               'CLASS_OLDACTIVITY', 'FILELAYOUT', 'PRINT', 'PRINTFILEREF', 'COMPONENTINTERFACE', 'COMPINTFCINTERFACE',
               'COMPINTFCPROPERTY', 'AESECTION', 'AESTEP', 'AEACTION', 'RULE', 'SQLTYPE', 'PCDEBUGGER',
               'SCROLL', 'EXESTATEMENT', 'APPRRULESET', 'REPORT', 'SUBSCRIPTION', 'LANGUAGETRANSLATIONS',
               'CLASS', 'HTML', 'IMAGE', 'ALTCONTNUM', 'DYNAMICPAGE', 'STYLESHEET', 'CONTTYPE', 'PATHREF',
               'FIELDTYPE', 'PORTALDEFINITIONNAME', 'PORTALSTRUCTURENAME', 'PORTALREFTYPE', 'PORTALOBJNAME',
               'LABELNAME', 'URL', 'APPLICATION_PACKAGE', 'APPLICATION_PACKAGE1', 'APPLICATION_PACKAGE2',
               'APPLICATION_CLASS', 'PORTALUSERHOMEPAGE', 'PROBTYPE', 'AEDEBUGGER', 'MOBILEPAGE', 'PSARCH_ID',
               'SQL', 'PORTALUSERFAVORITE', 'PORTALLABELNAME', 'PACKAGEROOT', 'PACKAGEQUALIFYPATH', 'RELATIONSHIPID',
               'MCFIMInfo', 'OPTMODEL', 'FILEREFERENCE', 'TYPECODE', 'PSARCH_OBJECT', 'PACKAGEID', 'CONTNAME',
               'ANALYTIC_MODEL_ID', 'TRANSLATE', 'VISUALCOMPARE_PAGE', 'PCODEWIP', 'MERGE', 'ETLINFO', 'WSRPPRODUCERNAME',
               'WSRPPORTLETNAME', 'JPLT_APPNAME', 'JPLT_NAME', 'TRANSACTIONTYPE', 'MESSAGEVERSION' ]

pCNameToParentAsCIAType = [ None, "Record", "Menu", "Page", "Component", "Component", "Component", "Application Engine",
                            "Component Interface", "Message", "Message", "Message Channel", "Page", "Application Package",
                            "Application Package", "Application Package", "Component Interface", "Component Interface",
                            "Component Interface", "Component Interface"]
