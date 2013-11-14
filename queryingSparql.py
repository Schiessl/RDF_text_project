###
# Using sparql
###
import rdflib
from rdflib import plugin
from rdflib.graph import Graph
import sys,traceback

#Variables to edit manually
path = '/Users/marceloschiessl/Documents/workspaceWTA/NLP prog/dados/TESTES ONTOLOGIA/'
file_name = 'example_schematriples' 
extOnto = '.owl'
extTxt = '.txt'
aspas = '"'

ontoFile = path + file_name + extOnto
 
g = Graph()
g.parse(ontoFile)#do not modify anything here!
# from rdflib.namespace import Namespace
# ns = Namespace("http://oaei.ontologymatching.org/2011/benchmarks/101/onto.rdf#")
 
plugin.register(
    'sparql', rdflib.query.Processor,
    'rdfextras.sparql.processor', 'Processor')
plugin.register(
    'sparql', rdflib.query.Result,
    'rdfextras.sparql.query', 'SPARQLQueryResult')
#
qres = g.query(
                """
                    SELECT DISTINCT ?varClass ?varSubClass ?varSubClassComment ?varProperty ?varPropComment
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
#                 , initNs=dict(
#                                 ns=Namespace("http://oaei.ontologymatching.org/2011/benchmarks/101/onto.rdf#")
#                               )
               )

for row in qres.result:
    print ("%s %s %s %s %s" % row) # %s represent the fields selected in the query

# print (len(qres.result)) #rows in the file
#
## Creating documents to compare
## It creates text files with the result of sparql query
textFile = path + file_name + extTxt

def createPhysicalFile(stringPath):
#creating physical file
    try:
        to_file = open(stringPath, 'w') #opening the file to write
        print>>to_file, 'varClass varClass varSubClass varSubClassComment varProperty varPropComment' #creating header
        for row in qres.result:
            print>>to_file, ("%s %s %s %s %s" % row) #creating body
        to_file.close() #closing the file
        return 'File created successfully ', str(len(qres.result)) + ' lines', True, 
    except:
        print "Error found:"
        traceback.print_exc(file=sys.stdout)
        return False

print createPhysicalFile(textFile)