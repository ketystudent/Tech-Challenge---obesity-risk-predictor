# Dicionario de Dados

Dataset: `data/raw/Obesity.csv`

O objetivo e prever a coluna `Obesity`, que representa o nivel de obesidade/peso do paciente.

| Coluna | Tipo | Descricao | Exemplos/escala |
|---|---|---|---|
| `Gender` | Categórica | Genero informado. | `Male`, `Female` |
| `Age` | Numérica | Idade em anos. | 14 a 61 |
| `Height` | Numérica | Altura em metros. | 1.45 a 1.98 |
| `Weight` | Numérica | Peso em kg. | 39 a 173 |
| `family_history` | Categórica | Historico familiar de excesso de peso. | `yes`, `no` |
| `FAVC` | Categórica | Consumo frequente de alimentos altamente caloricos. | `yes`, `no` |
| `FCVC` | Numérica ordinal | Frequencia de consumo de vegetais. | 1 a 3 |
| `NCP` | Numérica ordinal | Quantidade de refeicoes principais por dia. | 1 a 4 |
| `CAEC` | Categórica ordinal | Consumo de alimentos entre refeicoes. | `no`, `Sometimes`, `Frequently`, `Always` |
| `SMOKE` | Categórica | Indicador se fuma. | `yes`, `no` |
| `CH2O` | Numérica ordinal | Consumo diario de agua. | 1 a 3 |
| `SCC` | Categórica | Monitoramento de calorias ingeridas. | `yes`, `no` |
| `FAF` | Numérica ordinal | Frequencia de atividade fisica. | 0 a 3 |
| `TUE` | Numérica ordinal | Tempo de uso de dispositivos tecnologicos. | 0 a 2 |
| `CALC` | Categórica ordinal | Frequencia de consumo de alcool. | `no`, `Sometimes`, `Frequently`, `Always` |
| `MTRANS` | Categórica | Meio de transporte usual. | `Walking`, `Bike`, `Motorbike`, `Automobile`, `Public_Transportation` |
| `Obesity` | Alvo | Classe de peso/obesidade a prever. | 7 classes |

## Classes do Alvo

| Classe | Interpretacao |
|---|---|
| `Insufficient_Weight` | Peso insuficiente |
| `Normal_Weight` | Peso normal |
| `Overweight_Level_I` | Sobrepeso nivel I |
| `Overweight_Level_II` | Sobrepeso nivel II |
| `Obesity_Type_I` | Obesidade tipo I |
| `Obesity_Type_II` | Obesidade tipo II |
| `Obesity_Type_III` | Obesidade tipo III |

## Features Criadas na Pipeline

| Feature | Origem | Observacao |
|---|---|---|
| `BMI` | `Weight / Height^2` | Sinal clinico forte; pode aumentar muito o desempenho. |
| `BMI_Class` | Faixas fixas de IMC | Criada com `pd.cut`, sem aprender quantis da base inteira. |
| `Faixa_Etaria` | Faixas fixas de idade | Criada com limites fixos. |
| `Weight_Class` | Faixas fixas de peso | Usada no modelo completo; considerada redundante em cenarios alternativos. |
| `Active_Lifestyle` | `FAF >= 2` | Indicador binario de atividade fisica. |
| `Healthy_Diet` | `FCVC >= 2` e `FAVC == no` | Indicador binario de padrao alimentar mais saudavel. |
| `Good_Hydration` | `CH2O >= 2` | Indicador binario de hidratacao. |
| `High_Screen_Time` | `TUE >= 2` | Indicador binario de alto tempo de tela. |
| `Healthy_Score` | Soma de indicadores | Pontuacao simples de habitos saudaveis. |

