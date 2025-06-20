# PARA SIMPLE QUERIES

# 1º PASSO: PRODUZIR RESULTADOS SOLR
# Produzir resultados para no schema
./scripts/query_solr.py --query config/simple_queries/no_schema/queries/query3.json --uri http://localhost:8983/solr --collection wikiwar > config/simple_queries/no_schema/results/result_query_No_Schema_Simple4.json

# Produzir resultados para simple schema
./scripts/query_solr.py --query config/simple_queries/simple_schema/queries/query3.json --uri http://localhost:8983/solr --collection wikiwar > config/simple_queries/simple_schema/results/result_query_SchemaSimple_Simple4.json

# Produzir resultados para boosted schema
./scripts/query_solr.py --query config/simple_queries/boosted_schema/queries/query3.json --uri http://localhost:8983/solr --collection wikiwar > config/simple_queries/boosted_schema/results/result_query_SchemaBoosted_Simple4.json


# 2º PASSO: CONVERTER RESULTADOS SOLR PARA FORMATO TREC
# Produzir resultados para no schema
./scripts/query_solr.py --query config/simple_queries/no_schema/results/result_query3.json --uri http://localhost:8983/solr --collection wikiwar | ./scripts/solr2trec.py > config/simple_queries/no_schema/qrels/result_query3_trec.txt

# Produzir resultados para simple schema
./scripts/query_solr.py --query config/simple_queries/simple_schema/queries/query1.json --uri http://localhost:8983/solr --collection wikiwar | ./scripts/solr2trec.py > config/simple_queries/simple_schema/qrels/result_query1_trec.txt

# Produzir resultados para boosted schema
./scripts/query_solr.py --query config/simple_queries/boosted_schema/queries/query1.json --uri http://localhost:8983/solr --collection wikiwar | ./scripts/solr2trec.py > config/simple_queries/boosted_schema/qrels/result_query1_trec.txt


# 3º PASSO: CONVERTER QRELS PARA FORMATO TREC
# Produzir resultados para no schema
cat config/simple_queries/no_schema/qrels/qrels3.txt | ./scripts/qrels2trec.py > config/simple_queries/no_schema/qrels/qrels_trec_No_Schema_Simple4.txt

# Produzir resultados para simple schema
cat config/simple_queries/simple_schema/qrels/qrels3.txt | ./scripts/qrels2trec.py > config/simple_queries/simple_schema/qrels/qrrels_trec_SchemaSimple_Simple4.txt

# Produzir resultados para boosted schema
cat config/simple_queries/boosted_schema/qrels/qrels3.txt | ./scripts/qrels2trec.py > config/simple_queries/boosted_schema/qrels/qrels_trec_SchemaBoosted_Simple4.txt



# 4º PASSO: AVALIAR RESULTADOS
# Avaliar resultados para no schema
src/trec_eval/trec_eval config/simple_queries/no_schema/qrels/qrels_trec_No_Schema_Simple4.txt config/simple_queries/no_schema/qrels/results_trec_No_Schema_Simple4.txt

# Avaliar resultados para simple schema
src/trec_eval/trec_eval config/simple_queries/simple_schema/qrels/qrels_trec_SchemaSimple_Simple4.txt config/simple_queries/simple_schema/qrels/results_trec_SchemaSimple_Simple4.txt

# Avaliar resultados para boosted schema
src/trec_eval/trec_eval config/simple_queries/boosted_schema/qrels/qrels_trec_SchemaBoosted_Simple4.txt config/simple_queries/boosted_schema/qrels/results_trec_SchemaBoosted_Simple4.txt

# 5º PASSO: PLOTAR PRECISION-RECALL
# Plotar precision-recall para no schema
cat config/simple_queries/no_schema/qrels/results_trec_No_Schema_Simple4.txt | ./scripts/plot_pr.py --qrels config/simple_queries/no_schema/qrels/qrels_trec_No_Schema_Simple4.txt --output config/simple_queries/no_schema/images/p_r_graph_no_schema4.png

# Plotar precision-recall para simple schema
cat config/simple_queries/simple_schema/qrels/results_trec_SchemaSimple_Simple4.txt | ./scripts/plot_pr.py --qrels config/simple_queries/simple_schema/qrels/qrels_trec_SchemaSimple_Simple4.txt --output config/simple_queries/simple_schema/images/p_r_graph_simple_schema4.png

# Plotar precision-recall para boosted schema
cat config/simple_queries/boosted_schema/qrels/results_trec_SchemaBoosted_Simple4.txt | ./scripts/plot_pr.py --qrels config/simple_queries/boosted_schema/qrels/qrels_trec_SchemaBoosted_Simple4.txt --output config/simple_queries/boosted_schema/images/p_r_graph_boosted_schema4.png



# PARA PARA BOOSTED QUERIES

# 1º PASSO: PRODUZIR RESULTADOS SOLR
# Produzir resultados para no schema
./scripts/query_solr.py --query config/boosted_queries/no_schema/queries/query_boosted4.json --uri http://localhost:8983/solr --collection wikiwar > config/boosted_queries/no_schema/results/result_query_No_Schema_Boosted4.json

# Produzir resultados para simple schema
./scripts/query_solr.py --query config/boosted_queries/simple_schema/queries/query_boosted4.json --uri http://localhost:8983/solr --collection wikiwar > config/boosted_queries/simple_schema/results/result_query_SchemaSimple_Boosted4.json

# Produzir resultados para boosted schema
./scripts/query_solr.py --query config/boosted_queries/boosted_schema/queries/query_boosted4.json --uri http://localhost:8983/solr --collection wikiwar > config/boosted_queries/boosted_schema/results/result_query_SchemaBoosted_Boosted4.json

# 3º PASSO: CONVERTER QRELS PARA FORMATO TREC

# Produzir resultados para no schema
cat config/boosted_queries/no_schema/qrels/qrels3.txt | ./scripts/qrels2trec.py > config/boosted_queries/no_schema/qrels/qrels_trec_No_Schema_Boosted4.txt

# Produzir resultados para simple schema
cat config/boosted_queries/simple_schema/qrels/qrels3.txt | ./scripts/qrels2trec.py > config/boosted_queries/simple_schema/qrels/qrels_trec_SchemaSimple_Boosted4.txt

# Produzir resultados para boosted schema
cat config/boosted_queries/boosted_schema/qrels/qrels3.txt | ./scripts/qrels2trec.py > config/boosted_queries/boosted_schema/qrels/qrels_trec_SchemaBoosted_Boosted4.txt


# 4º PASSO: AVALIAR RESULTADOS

# Avaliar resultados para no schema 
src/trec_eval/trec_eval config/boosted_queries/no_schema/qrels/qrels_trec_No_Schema_Boosted4.txt config/boosted_queries/no_schema/qrels/results_trec_No_Schema_Boosted4.txt

# Avaliar resultados para simple schema
src/trec_eval/trec_eval config/boosted_queries/simple_schema/qrels/qrels_trec_SchemaSimple_Boosted4.txt config/boosted_queries/simple_schema/qrels/results_trec_SchemaSimple_Boosted4.txt

# Avaliar resultados para boosted schema
src/trec_eval/trec_eval config/boosted_queries/boosted_schema/qrels/qrels_trec_SchemaBoosted_Boosted4.txt config/boosted_queries/boosted_schema/qrels/results_trec_SchemaBoosted_Boosted4.txt

# 5º PASSO: PLOTAR PRECISION-RECALL
# Plotar precision-recall para no schema
cat config/boosted_queries/no_schema/qrels/results_trec_No_Schema_Boosted4.txt | ./scripts/plot_pr.py --qrels config/boosted_queries/no_schema/qrels/qrels_trec_No_Schema_Boosted4.txt --output config/boosted_queries/no_schema/images/p_r_graph_no_schema_boosted4.png

# Plotar precision-recall para simple schema
cat config/boosted_queries/simple_schema/qrels/results_trec_SchemaSimple_Boosted4.txt | ./scripts/plot_pr.py --qrels config/boosted_queries/simple_schema/qrels/qrels_trec_SchemaSimple_Boosted4.txt --output config/boosted_queries/simple_schema/images/p_r_graph_simple_schema_boosted4.png

# Plotar precision-recall para boosted schema
cat config/boosted_queries/boosted_schema/qrels/results_trec_SchemaBoosted_Boosted4.txt | ./scripts/plot_pr.py --qrels config/boosted_queries/boosted_schema/qrels/qrels_trec_SchemaBoosted_Boosted4.txt --output config/boosted_queries/boosted_schema/images/p_r_graph_boosted_schema_boosted4.png