# Datasets para Comparação: Tetris vs Tetris Mobilidade

Este conjunto de datasets foi criado especificamente para demonstrar as diferenças de desempenho entre o algoritmo **Tetris original** e o **Tetris com Mobilidade** no EdgeSimPy.

## Contexto dos Algoritmos

### Tetris Original
- **Critério de alocação**: Apenas recursos disponíveis (CPU, memória, disco)
- **Ordenação**: Média geométrica dos recursos disponíveis
- **Limitações**: Não considera localização geográfica dos usuários

### Tetris Mobilidade  
- **Critério de alocação**: Recursos + proximidade geográfica + previsão de movimento
- **Pontuação**: 60% proximidade + 40% recursos
- **Vantagens**: Considera mobilidade e localização dos usuários

## Datasets Criados

### Dataset 1: `dataset_tetris_vs_mobilidade_1.json`
**Cenário**: Servidores potentes distantes vs. servidores próximos com poucos recursos

**Características**:
- **Usuários**: 4 usuários móveis em 2 grupos geográficos
  - Grupo 1: Usuários 1 e 2 em [5, 2] - SLAs: 30ms e 25ms
  - Grupo 2: Usuários 3 e 4 em [15, 8] - SLAs: 35ms e 20ms

- **Servidores**:
  - Servidor 1 [0, 0]: 32 CPU, 65GB RAM - **Distante dos usuários**
  - Servidor 2 [10, 10]: 64 CPU, 131GB RAM - **Muito distante dos usuários**
  - Servidor 3 [5, 2]: 4 CPU, 8GB RAM - **Próximo ao grupo 1, mas limitado**
  - Servidor 4 [15, 8]: 8 CPU, 16GB RAM - **Próximo ao grupo 2, mas limitado**

**Resultado Esperado**:
- **Tetris**: Escolherá servidores 1 e 2 (mais recursos) → Alto delay por distância
- **Tetris Mobilidade**: Escolherá servidores 3 e 4 (próximos) → Menor delay

### Dataset 2: `dataset_tetris_vs_mobilidade_2.json`
**Cenário**: Dispersão geográfica extrema

**Características**:
- **Usuários**: 5 usuários espalhados geograficamente
  - Usuários 1-2 em [3, 4] - SLAs: 40ms e 35ms
  - Usuário 3 em [22, 28] - SLA: 45ms  
  - Usuários 4-5 em [12, 15] - SLAs: 25ms e 30ms

- **Servidores**:
  - Servidor 1 [0, 0]: 256 CPU, 512GB RAM - **Mega servidor isolado**
  - Servidor 2 [25, 25]: 512 CPU, 1TB RAM - **Giga servidor isolado**
  - Servidor 3 [3, 4]: 2 CPU, 4GB RAM - **Próximo usuários 1-2**
  - Servidor 4 [22, 28]: 4 CPU, 8GB RAM - **Próximo usuário 3**
  - Base Station 5 [12, 15]: **Sem servidor** - Usuários 4-5 sem servidor local

**Resultado Esperado**:
- **Tetris**: Usará sempre servidores 1 e 2 → Delays enormes
- **Tetris Mobilidade**: Priorizará proximidade → Melhor distribuição

### Dataset 3: `dataset_tetris_vs_mobilidade_3.json`
**Cenário**: Aplicações de alta demanda com recursos massivos distantes

**Características**:
- **Usuários**: 3 usuários com aplicações intensivas
  - Usuário 1 [10, 5]: Streaming (12 CPU, 20GB RAM) - SLA: 50ms
  - Usuário 2 [40, 5]: Gaming (16 CPU, 32GB RAM) - SLA: 45ms
  - Usuário 3 [25, 10]: AR/VR (20 CPU, 40GB RAM) - SLA: 40ms

- **Servidores**:
  - Servidor 1 [0, 0]: 1024 CPU, 2TB RAM - **SuperComputer isolado**
  - Servidor 2 [50, 0]: 2048 CPU, 4TB RAM - **HyperComputer isolado**
  - Servidor 3 [10, 5]: 8 CPU, 16GB RAM - **Próximo usuário 1**
  - Servidor 4 [40, 5]: 16 CPU, 32GB RAM - **Próximo usuário 2**
  - Base Station 5 [25, 10]: **Sem servidor** - Usuário 3 sem servidor local

**Resultado Esperado**:
- **Tetris**: Usará servidores 1 e 2 → Delays de rede altíssimos (150ms+)
- **Tetris Mobilidade**: Balanceará entre proximidade e recursos → Melhor QoS

## Como Usar

1. **Execute simulações** com ambos os algoritmos nos mesmos datasets
2. **Compare métricas**:
   - Delay médio dos usuários
   - Violações de SLA
   - Utilização dos servidores
   - Consumo energético

3. **Análise esperada**:
   - Tetris Mobilidade deve ter **menores delays**
   - Tetris original deve ter **melhor utilização de recursos**
   - Trade-off entre eficiência de recursos vs. QoS

## Métricas Recomendadas

```python
# Métricas para análise
- user_delays: Delay experimentado pelos usuários  
- sla_violations: Número de violações de SLA
- server_utilization: Utilização de CPU/Memória dos servidores
- energy_consumption: Consumo energético total
- service_migrations: Número de migrações de serviços
```

## Conclusões Esperadas

Estes datasets foram projetados para mostrar que:

1. **Em cenários de mobilidade**, a proximidade geográfica é crucial
2. **O Tetris original** falha ao ignorar a localização dos usuários
3. **O Tetris Mobilidade** oferece melhor QoS em ambientes distribuídos
4. **Trade-off** entre eficiência de recursos e qualidade de serviço

Use estes datasets para validar que o algoritmo Tetris Mobilidade supera o Tetris original em cenários onde a mobilidade e a localização geográfica são fatores importantes. 