###
# Using sparql
###
import rdflib
from rdflib import plugin
from rdflib.graph import Graph
import sys,traceback

#Variables to edit manually
path = 'dados/TESTES ONTOLOGIA/'
file_name = 'example_schematriples' 
file_name = 'foaf' 
extOnto = '.rdf'
extTxt = '.txt'
outputFile = "%s %s %s %s %s %s %s %s %s %s" # %s represent the fields selected in the query

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
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT DISTINCT ?varClass  ?Allprop ?AllPropComment ?varSubClass ?varCommentSubclass ?ClasseRel ?SuperClass ?SuperClass ?varCommentSuperClass ?CommentClasseRel
                        WHERE { 
                                    ?varClass rdf:type owl:Class.
                                    {?Allprop rdf:type owl:ObjectProperty} UNION {?Allprop rdf:type owl:DatatypeProperty}.
                                    {?Allprop rdfs:domain ?varClass ; rdfs:range ?ClasseRel} UNION {?Allprop rdfs:range ?varClass ; rdfs:domain ?ClasseRel}. 
                                    OPTIONAL {?Allprop rdfs:comment ?AllPropComment}.
                                    OPTIONAL{?ClasseRel rdfs:comment ?CommentClasseRel}.
                                    OPTIONAL{?varSubClass rdfs:subClassOf ?varClass; OPTIONAL{?varSubClass rdfs:comment ?varCommentSubclass}}.
                                    OPTIONAL{?varClass rdfs:subClassOf ?SuperClass; OPTIONAL{?SuperClass rdfs:comment ?varCommentSuperClass}}
                               }
ORDER BY ?varClass
                """
#                 , initNs=dict(
#                                 ns=Namespace("http://oaei.ontologymatching.org/2011/benchmarks/101/onto.rdf#")
#                               )
               )

# qres = g.query(
#                 """
#                     SELECT DISTINCT ?varClass ?varSubClass ?varSubClassComment ?varProperty ?varPropComment
#                         WHERE { 
#                                 { 
#                                     ?varClass rdf:type owl:Class .
#                                     ?varProperty rdf:type owl:ObjectProperty ; rdfs:domain ?varClass . OPTIONAL{?varProperty rdfs:comment ?varPropComment} .
#                                     OPTIONAL{?varSubClass rdfs:subClassOf ?varClass ; rdfs:comment ?varSubClassComment} .
#                                     }
#                                     UNION
#                                     {
#                                     ?varClass rdf:type owl:Class .
#                                     ?varProperty rdf:type owl:DatatypeProperty ; rdfs:domain ?varClass . OPTIONAL{?varProperty rdfs:comment ?varPropComment}.
#                                 }
#                             }
#                 """
# #                 , initNs=dict(
# #                                 ns=Namespace("http://oaei.ontologymatching.org/2011/benchmarks/101/onto.rdf#")
# #                               )
#                )

for row in qres.result:
    print (outputFile % row) 

# print (len(qres.result)) #rows in the file
#
## Creating documents to compare
## It creates text files with the result of sparql query in order to be compared 
textFile = path + file_name + extTxt

def createPhysicalFile(stringPath):
#creating physical file
    try:
        to_file = open(stringPath, 'w') #opening the file to write
#         print>>to_file, 'class subclass commentclass labelclass property commentproperty labelproperty' #creating header
        for row in qres.result:
            print>>to_file, (outputFile % row) #creating body
        to_file.close() #closing the file
        return 'File created successfully ', str(len(qres.result)) + ' lines', True, 
    except:
        print "Error found:"
        traceback.print_exc(file=sys.stdout)
        return False

print createPhysicalFile(textFile)
