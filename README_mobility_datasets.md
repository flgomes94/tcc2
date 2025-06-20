# Datasets para Comparação: Tetris vs Tetris com Mobilidade

Este conjunto de datasets foi criado especificamente para demonstrar as vantagens do algoritmo **Tetris com Mobilidade** sobre o **Tetris original** no EdgeSimPy.

## Contexto dos Algoritmos

### Tetris Original
- **Critério de alocação**: Foca apenas nos recursos disponíveis (CPU, memória, disco)
- **Ordenação**: Utiliza média geométrica dos recursos disponíveis
- **Limitações**: Não considera a localização geográfica dos usuários ou padrões de mobilidade

### Tetris com Mobilidade
- **Critério de alocação**: Considera recursos + proximidade geográfica + previsão de movimento
- **Pontuação**: Combina proximidade geográfica com disponibilidade de recursos
- **Vantagens**: Otimiza a alocação considerando a mobilidade dos usuários e latência de rede

## Datasets Criados

### Dataset 1: `mobility_dataset_1.json`
**Cenário**: Usuários móveis com serviços de baixa latência

**Características**:
- **Grade de Rede**: Malha 5x5 de switches e estações base
- **Servidores**:
  - Servidores potentes nos cantos da grade (64 CPU, 128GB RAM)
  - Servidores médios no centro (8-16 CPU, 16-32GB RAM)
  - Servidores pequenos em locais estratégicos (4 CPU, 8GB RAM)
- **Usuários**:
  - Usuário 1: Aplicação VR com SLA de 15ms, próximo a servidor pequeno
  - Usuário 2: Aplicação de jogos com SLA de 10ms, próximo a servidor pequeno
  - Usuário 3: Aplicação AR com SLA de 5ms, no centro da grade
  - Usuário 4: Aplicação de streaming com SLA de 20ms, em movimento

**Resultado Esperado**:
- **Tetris Original**: Alocará serviços nos servidores maiores (cantos) → Maior latência
- **Tetris com Mobilidade**: Priorizará servidores próximos → Menor latência, cumprimento de SLAs

### Dataset 2: `mobility_dataset_2.json`
**Cenário**: Usuários movendo-se entre clusters de servidores

**Características**:
- Mesma infraestrutura do Dataset 1
- **Padrões de Mobilidade**:
  - Usuários se movem entre diferentes clusters de servidores
  - Exige migração de serviços para manter baixa latência

**Resultado Esperado**:
- **Tetris Original**: Alocação estática baseada apenas em recursos → Degradação de desempenho
- **Tetris com Mobilidade**: Realocação dinâmica seguindo o movimento → Manutenção da QoS

### Dataset 3: `mobility_dataset_3.json`
**Cenário**: Demandas de recursos variadas em diferentes áreas geográficas

**Características**:
- Mesma infraestrutura dos datasets anteriores
- **Demandas de Recursos**:
  - Serviço 1: Alto CPU (12), baixa memória (4GB)
  - Serviço 2: Baixo CPU (2), alta memória (24GB)
  - Serviço 3: Balanceado mas alto (8 CPU, 16GB)
  - Serviço 4: Muito baixo (1 CPU, 2GB)

**Resultado Esperado**:
- **Tetris Original**: Foco apenas na eficiência de recursos → Possível violação de SLAs
- **Tetris com Mobilidade**: Balanceamento entre recursos e proximidade → Melhor QoS geral

## Como Utilizar os Datasets

1. **Geração dos Datasets**:
   ```
   python generate_mobility_datasets.py
   ```

2. **Execução de Simulações**:
   - Execute simulações com ambos os algoritmos (Tetris e Tetris com Mobilidade)
   - Use os mesmos datasets para comparação direta

3. **Métricas para Análise**:
   - **Latência média**: Delay experimentado pelos usuários
   - **Violações de SLA**: Número de vezes que os requisitos de latência não foram atendidos
   - **Utilização de recursos**: Eficiência no uso de CPU e memória
   - **Migrações de serviço**: Quantidade de migrações necessárias
   - **Consumo energético**: Energia total consumida pela infraestrutura

## Características que Favorecem o Tetris com Mobilidade

1. **Requisitos Estritos de Latência**:
   - SLAs rigorosos que só podem ser cumpridos com servidores próximos

2. **Distribuição Geográfica**:
   - Usuários e servidores distribuídos em uma área ampla
   - Distâncias significativas entre clusters de servidores

3. **Padrões de Mobilidade**:
   - Usuários se movendo entre diferentes áreas da rede
   - Necessidade de prever movimentos para otimizar alocações

4. **Heterogeneidade de Recursos**:
   - Servidores com diferentes capacidades
   - Trade-off entre capacidade de recursos e proximidade geográfica

## Conclusão

Estes datasets foram projetados especificamente para demonstrar as vantagens do algoritmo Tetris com Mobilidade sobre o Tetris original em cenários onde a mobilidade dos usuários e a latência de rede são fatores críticos.

A expectativa é que o Tetris com Mobilidade apresente:
- Menor latência média
- Menos violações de SLA
- Melhor experiência do usuário
- Maior adaptabilidade a padrões de mobilidade

Embora o Tetris original possa apresentar melhor utilização de recursos em alguns casos, o Tetris com Mobilidade deve demonstrar um melhor equilíbrio entre eficiência de recursos e qualidade de serviço. 