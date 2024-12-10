                                df_exercicio_count = dataset.groupby(['nome', 'ponto'])['numero_serie'].count().reset_index()

                                # Ordenando por número de séries
                                df_exercicio_count = df_exercicio_count.sort_values(by='numero_serie', ascending=False)

                                # Separando os dados por ponto (Cima e Baixo)
                                df_cima = df_exercicio_count[df_exercicio_count['ponto'] == 'Cima']
                                df_baixo = df_exercicio_count[df_exercicio_count['ponto'] == 'Baixo']

                                # Criando gráfico de barras para cada ponto
                                st.bar_chart(df_cima.set_index('nome')['numero_serie'], use_container_width=True)
                                st.bar_chart(df_baixo.set_index('nome')['numero_serie'], use_container_width=True)

                                # Peso médio por exercício
                                df_exercicio_weight = dataset.groupby('nome')['peso'].mean().reset_index()
                                st.bar_chart(df_exercicio_weight.set_index('nome')['peso'])

                                # Distribuição de séries por grupo muscular
                                df_group_muscular = dataset.groupby('grupo_muscular')['numero_serie'].sum().reset_index()
                                st.bar_chart(df_group_muscular.set_index('grupo_muscular')['numero_serie'])


                                # Evolução de massa e altura por data de sessão
                                df_progresso = dataset.groupby('data_sessao')[['massa', 'altura']].mean().reset_index()

                                # Gráfico de evolução de massa e altura
                                st.line_chart(df_progresso.set_index('data_sessao'))


                                # Tempo total por exercício
                                df_exercicio_time = dataset.groupby('nome')['tempo'].sum().reset_index()
                                st.bar_chart(df_exercicio_time.set_index('nome')['tempo'])

                                # Analisando intensidade como uma combinação de peso e tempo
                                dataset['intensidade'] = dataset['peso'] * dataset['tempo']  # Peso x Tempo como uma métrica de intensidade
                                df_exercicio_intensity = dataset.groupby('nome')['intensidade'].sum().reset_index()
                                st.bar_chart(df_exercicio_intensity.set_index('nome')['intensidade'])
 
                                # Analisando a distribuição de exercícios por lado
                                df_lado = dataset.groupby('lado')['numero_serie'].sum().reset_index()
                                st.bar_chart(df_lado.set_index('lado')['numero_serie'])

                                # Encontrar as sessões com menor e maior tempo total
                                min_sessao = dataset.loc[dataset['tempo_total'].idxmin()]
                                max_sessao = dataset.loc[dataset['tempo_total'].idxmax()]

                                st.write(f"Sessão com menor tempo: {min_sessao['data_sessao']} - {min_sessao['tempo_total']} minutos")
                                st.write(f"Sessão com maior tempo: {max_sessao['data_sessao']} - {max_sessao['tempo_total']} minutos")


                                # Contabilizando o número de séries por sessão
                                df_sessoes_series = dataset.groupby('data_sessao')['numero_serie'].sum().reset_index()
                                st.bar_chart(df_sessoes_series.set_index('data_sessao')['numero_serie'])

                                # Desempenho do paciente por grupo muscular
                                df_performance = dataset.groupby('grupo_muscular')['numero_serie'].sum().reset_index()
                                st.bar_chart(df_performance.set_index('grupo_muscular')['numero_serie'])


                                # Resumo geral
                                resumo = dataset[['tempo_total', 'numero_serie', 'peso']].agg(['mean', 'sum']).reset_index()
                                st.table(resumo)
