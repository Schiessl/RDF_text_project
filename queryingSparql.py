###
# Using sparql
###
import rdflib
from rdflib import plugin
from rdflib.graph import Graph
import sys,traceback
 
g = Graph()
# g.parse("/Users/marceloschiessl/Documents/workspaceWTA/NLP prog/dados/TESTES ONTOLOGIA/101 - DR1/DSO- 101-1 A.owl")
# g.parse("/Users/marceloschiessl/Documents/workspaceWTA/NLP prog/dados/TESTES ONTOLOGIA/Onto 2 - grupo 1/104/onto 2- 104.rdf")
g.parse("/Users/marceloschiessl/Documents/workspaceWTA/NLP prog/dados/TESTES ONTOLOGIA/Onto 2 - grupo 1/203/onto 2 - 203.rdf")
from rdflib.namespace import Namespace
ns = Namespace("http://oaei.ontologymatching.org/2011/benchmarks/101/onto.rdf#")
 
plugin.register(
    'sparql', rdflib.query.Processor,
    'rdfextras.sparql.processor', 'Processor')
plugin.register(
    'sparql', rdflib.query.Result,
    'rdfextras.sparql.query', 'SPARQLQueryResult')
#
qres = g.query(
                """
                    SELECT  DISTINCT ?varClass ?varSubClass ?varSubClassComment ?varProperty ?varPropComment
                        WHERE { 
                                { 
                                    ?varClass rdf:type owl:Class .
                                    ?varProperty rdf:type owl:ObjectProperty ; rdfs:domain ?varClass . OPTIONAL{?varProperty rdfs:comment ?varPropComment} .
                                    OPTIONAL{?varSubClass rdfs:subClassOf ?varClass ; rdfs:comment ?varSubClassComment} .
                                    }
                                    UNION
                                    {
                                    ?varClass rdf:type owl:Class .
                                    ?varProperty rdf:type owl:DatatypeProperty ; rdfs:domain ?varClass . OPTIONAL{?varProperty rdfs:comment ?varPropComment}.
                                }
                            }
                """
                , initNs=dict(
                                ns=Namespace("http://oaei.ontologymatching.org/2011/benchmarks/101/onto.rdf#")
                              )
               )

for row in qres.result:
    print ("%s %s %s %s %s" % row) # %s represent the fields selected in the query

print (len(qres.result)) #rows in the file
#
## Creating documents to compare
## It creates text files with the result of sparql query in order to be compared 
path = '//Users/marceloschiessl/Documents/workspaceWTA/NLP prog/dados/TESTES ONTOLOGIA/'
file_name = 'doc3' 
file_created = path + file_name + '.txt'

def createPhysicalFile(stringPath):
#creating physical file
    try:
        to_file = open(stringPath, 'w') #opening the file to write
        print>>to_file, 'varClass varClass varSubClass varSubClassComment varProperty varPropComment' #creating header
        for row in qres.result:
            print>>to_file, ("%s %s %s %s %s" % row) #creating body
        to_file.close() #closing the file
        return True
    except:
        print "Error found:"
        traceback.print_exc(file=sys.stdout)
        return False

print createPhysicalFile(file_created)