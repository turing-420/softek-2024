document.addEventListener('DOMContentLoaded', async () => {
    const dataFiles = [
        '/data/aberturas_encerrados.json',
        '/data/encerrados_complexidade.json',
        '/data/senioridade_custo.json',
        '/data/leadtime_mes_a_mes.json',
        '/data/acompanhamento_da_redistribuicao.json',
        '/data/encerramento_senioridade.json'
    ];
    let cuboData = {};
    let chartInstances = {};

    async function loadJSONData(filePaths) {
        try {
            const promises = filePaths.map(filePath => fetch(filePath).then(response => response.json()));
            const [aberturasEncerradosData, encerradosComplexidadeData, senioridadeCustoData, leadtimeMesData, acompanhamentoRedistribuicaoData, encerramentoSenioridadeData] = await Promise.all(promises);
            
            console.log('Data loaded successfully:', { aberturasEncerradosData, encerradosComplexidadeData, senioridadeCustoData, leadtimeMesData, acompanhamentoRedistribuicaoData, encerramentoSenioridadeData });
            
            return {
                cubo1Data: aberturasEncerradosData,
                cubo2Data: encerradosComplexidadeData,
                cubo3Data: leadtimeMesData,
                senioridadeCustoData: senioridadeCustoData,
                acompanhamentoRedistribuicaoData: acompanhamentoRedistribuicaoData,
                encerramentoSenioridadeData: encerramentoSenioridadeData
            };
        } catch (error) {
            console.error('Error loading JSON data:', error);
            return {
                cubo1Data: [],
                cubo2Data: [],
                cubo3Data: [],
                senioridadeCustoData: [],
                acompanhamentoRedistribuicaoData: [],
                encerramentoSenioridadeData: []
            };
        }
    }

    function updateFilters() {
        if (!cuboData) return;

        const anomesOptions = cuboData.cubo1Data ? [...new Set(cuboData.cubo1Data.map(row => row.ANOMES_REF))] : [];

        const senioridadeOptions = ['Bg', 'Ex', 'Jr', 'Pr', 'Sr'];

        const complexidadeOptions = ['N1', 'N2', 'N3'];

        const areaOptions = cuboData.acompanhamentoRedistribuicaoData ? 
            [...new Set(cuboData.acompanhamentoRedistribuicaoData.map(row => row.MODULO_CHAMADO).filter(value => value && value.trim() !== ''))] : [];

        updateSelectOptions('anomes-filter', anomesOptions);
        updateSelectOptions('senioridade-filter', senioridadeOptions);
        updateSelectOptions('complexidade-filter', complexidadeOptions);
        updateSelectOptions('area-filter', areaOptions);
    }

    function updateSelectOptions(selectId, options) {
        const select = document.getElementById(selectId);
        select.innerHTML = '<option value="">Todos</option>';
        options.forEach(option => {
            if (option) {
                const optionElement = document.createElement('option');
                optionElement.value = option;
                optionElement.textContent = option;
                select.appendChild(optionElement);
            }
        });
        console.log(`${selectId} populated with options:`, options);
    }

    function applyFilters(data) {
    const anomesFilter = document.getElementById('anomes-filter').value;
    const senioridadeFilter = document.getElementById('senioridade-filter').value;
    const complexidadeFilter = document.getElementById('complexidade-filter').value;
    const areaFilter = document.getElementById('area-filter').value;

    let filteredData = {
        cubo1Data: data.cubo1Data || [],
        cubo2Data: data.cubo2Data || [],
        cubo3Data: data.cubo3Data || [],
        senioridadeCustoData: data.senioridadeCustoData || [],
        acompanhamentoRedistribuicaoData: data.acompanhamentoRedistribuicaoData || [],
        encerramentoSenioridadeData: data.encerramentoSenioridadeData || []
    };

    if (anomesFilter) {
        filteredData.cubo1Data = filteredData.cubo1Data.filter(item => item.ANOMES_REF === anomesFilter);
        filteredData.cubo2Data = filteredData.cubo2Data.filter(item => item.ANOMES_REF === anomesFilter);
        filteredData.cubo3Data = filteredData.cubo3Data.filter(item => item.ANOMES_REF === anomesFilter);
        filteredData.senioridadeCustoData = filteredData.senioridadeCustoData.filter(item => item.ANOMES_STATUS === anomesFilter);
        filteredData.encerramentoSenioridadeData = filteredData.encerramentoSenioridadeData.filter(item => item.ANOMES_REF === anomesFilter);
        filteredData.acompanhamentoRedistribuicaoData = filteredData.acompanhamentoRedistribuicaoData.filter(item => item.ANOMES_ABERTURA === anomesFilter);
    }

    if (senioridadeFilter) {
        filteredData.senioridadeCustoData = filteredData.senioridadeCustoData.map(item => {
            const newItem = { ANOMES_STATUS: item.ANOMES_STATUS };
            ['Bg', 'Ex', 'Jr', 'Pr', 'Sr'].forEach(role => {
                newItem[role] = (role === senioridadeFilter) ? item[role] : 0;
            });
            return newItem;
        });

        filteredData.encerramentoSenioridadeData = filteredData.encerramentoSenioridadeData.map(item => {
            const newItem = { ANOMES_REF: item.ANOMES_REF };
            ['Bg', 'Ex', 'Jr', 'Pr', 'Sr'].forEach(role => {
                newItem[role] = (role === senioridadeFilter) ? item[role] : 0;
            });
            return newItem;
        });
    }

    if (complexidadeFilter) {
        filteredData.cubo2Data = filteredData.cubo2Data.map(item => {
            const newItem = { ANOMES_REF: item.ANOMES_REF };
            ['N1', 'N2', 'N3'].forEach(level => {
                newItem[level] = (level === complexidadeFilter) ? item[level] : 0;
            });
            return newItem;
        });
        filteredData.acompanhamentoRedistribuicaoData = filteredData.acompanhamentoRedistribuicaoData.filter(item => item.COMPLEXIDADE === complexidadeFilter);
    }

    if (areaFilter) {
        filteredData.acompanhamentoRedistribuicaoData = filteredData.acompanhamentoRedistribuicaoData.filter(item => item.MODULO_CHAMADO === areaFilter);
    }

    return filteredData;
    }

    function createCharts(data) {
        if (!data) {
            console.error("No data provided to create charts");
            return;
        }

        // Aberturas x Encerramento
        if (data.cubo1Data && data.cubo1Data.length) {
            createAberturaEncerramentoChart(data.cubo1Data);
        }

        // Encerrados x Complexidade
        if (data.cubo2Data && data.cubo2Data.length) {
            createEncerradosComplexidadeChart(data.cubo2Data);
        }

        // Cargo x Custo Médio por Demanda
        if (data.senioridadeCustoData && data.senioridadeCustoData.length) {
            createCargoCustoChart(data.senioridadeCustoData);
        }

        // Encerramentos x Cargo
        if (data.encerramentoSenioridadeData && data.encerramentoSenioridadeData.length) {
            createEncerramentosCargoChart(data.encerramentoSenioridadeData);
        }

        // Additional Chart (Ocorrências Pendentes Redistribuídas)
        if (data.acompanhamentoRedistribuicaoData && data.acompanhamentoRedistribuicaoData.length) {
            createPendentesRedistribuidasChart(data.acompanhamentoRedistribuicaoData);
        }

        // Leadtime
        if (data.cubo3Data && data.cubo3Data.length) {
            createLeadTimeTable(data.cubo3Data);
        } else {
            console.error('cubo3Data is empty or undefined');
        }
    }

    function createPendentesRedistribuidasChart(data) {
        const ctx = document.getElementById('pendentes-redistribuidas-chart').getContext('2d');

        const anomesList = [...new Set(data.map(item => item.ANOMES_ABERTURA))];
        const complexidades = ['N1', 'N2', 'N3'];

        const datasets = complexidades.map(complexidade => {
            const dataCounts = anomesList.map(anomes => {
                return data.filter(item => item.ANOMES_ABERTURA === anomes && item.COMPLEXIDADE === complexidade).length;
            });
            return {
                label: complexidade,
                data: dataCounts,
                backgroundColor: getColorForComplexidade(complexidade),
                borderColor: getColorForComplexidade(complexidade, true),
                borderWidth: 1
            };
        });

        if (chartInstances.pendentesRedistribuidas) {
            chartInstances.pendentesRedistribuidas.destroy();
        }

        chartInstances.pendentesRedistribuidas = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: anomesList,
                datasets: datasets
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Volumetria'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Mês de Abertura'
                        }
                    }
                },
                plugins: {
                    title: {
                        display: true,
                        text: 'Ocorrências Pendentes Redistribuídas'
                    }
                }
            }
        });
    }

    function getColorForComplexidade(complexidade, border = false) {
        const colors = {
            'N1': 'rgba(54, 162, 235, 0.6)',
            'N2': 'rgba(255, 99, 132, 0.6)',
            'N3': 'rgba(75, 192, 192, 0.6)'
        };
        const borderColors = {
            'N1': 'rgba(54, 162, 235, 1)',
            'N2': 'rgba(255, 99, 132, 1)',
            'N3': 'rgba(75, 192, 192, 1)'
        };
        return border ? borderColors[complexidade] : colors[complexidade];
    }

    function createEncerramentosCargoChart(data) {
        const ctx = document.getElementById('encerramentos-cargo-chart').getContext('2d');

        const periods = data.map(item => item.ANOMES_REF);

        const roles = ['Bg', 'Ex', 'Jr', 'Pr', 'Sr'];

        const datasets = roles.map(role => {
            return {
                label: role,
                data: data.map(item => item[role] || 0),
                backgroundColor: getColorForSeniority(role, 0.6),
                borderColor: getColorForSeniority(role, 1),
                borderWidth: 1
            };
        });

        if (chartInstances.encerramentosCargo) {
            chartInstances.encerramentosCargo.destroy();
        }

        chartInstances.encerramentosCargo = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: periods,
                datasets: datasets
            },
            options: {
                scales: {
                    x: {
                        stacked: true,
                        title: {
                            display: true,
                            text: 'Período (ANOMES_REF)'
                        }
                    },
                    y: {
                        stacked: true,
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Número de Encerramentos'
                        }
                    }
                },
                plugins: {
                    title: {
                        display: true,
                        text: 'Encerramentos x Senioridade'
                    },
                    legend: {
                        display: true
                    },
                    datalabels: {
                        anchor: 'center',
                        align: 'center',
                        color: 'rgba(0, 0, 0, 0.6)',
                        font: {
                            weight: 'bold'
                        }
                    }
                },
                layout: {
                    padding: {
                        right: 10,
                        bottom: 10
                    }
                }
            },
            plugins: [ChartDataLabels]
        });
    }

    function getColorForSeniority(seniority, opacity = 1) {
        const colors = {
            'Bg': `rgba(0, 63, 92, ${opacity})`,
            'Ex': `rgba(122, 81, 149, ${opacity})`,
            'Jr': `rgba(239, 86, 117, ${opacity})`,
            'Pr': `rgba(255, 166, 0, ${opacity})`,
            'Sr': `rgba(44, 160, 44, ${opacity})`
        };
        return colors[seniority] || `rgba(0, 0, 0, ${opacity})`;
    }

    function createCargoCustoChart(data) {
    const ctx = document.getElementById('cargo-custo-chart').getContext('2d');

    const roles = ['Bg', 'Ex', 'Jr', 'Pr', 'Sr'];
    const periods = [...new Set(data.map(item => item.ANOMES_STATUS))];

    const datasets = periods.map((period, index) => {
        const periodData = data.find(item => item.ANOMES_STATUS === period) || {};
        const values = roles.map(role => parseFloat(periodData[role]) || 0);

        return {
            label: period,
            data: values,
            backgroundColor: getBackgroundColor(index),
            borderColor: getBorderColor(index),
            borderWidth: 1
        };
    });

    if (chartInstances.cargoCusto) {
        chartInstances.cargoCusto.destroy();
    }

    chartInstances.cargoCusto = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: roles,
            datasets: datasets
        },
        options: {
            indexAxis: 'y',
            scales: {
                x: {
                    stacked: true,
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Custo Médio por Demanda'
                    },
                    ticks: {
                        callback: function(value) {
                            return Number.isInteger(value) ? value : null;
                        }
                    }
                },
                y: {
                    stacked: true,
                    title: {
                        display: true,
                        text: 'Senioridade'
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Senioridade x Custo Médio por Demanda'
                },
                legend: {
                    display: true
                },
            datalabels: {
                anchor: 'center',
                align: 'center',
                color: 'rgba(0, 0, 0, 0.6)',
                font: {
                    weight: 'bold'
                },
                formatter: function(value) {
                    return value.toFixed(1);
                }
            }
            }
        },
        plugins: [ChartDataLabels]
    });
}

    function getBackgroundColor(index) {
    const colors = [
        'rgba(0, 123, 255, 0.3)',
        'rgba(255, 0, 0, 0.3)',  
        'rgba(0, 255, 0, 0.3)',  
        'rgba(255, 165, 0, 0.3)',
        'rgba(128, 0, 128, 0.3)' 
    ];
    return colors[index % colors.length];
    }

    function getBorderColor(index) {
    const colors = [
        'rgba(0, 123, 255, 0.8)',
        'rgba(255, 0, 0, 0.8)',  
        'rgba(0, 255, 0, 0.8)',  
        'rgba(255, 165, 0, 0.8)',
        'rgba(128, 0, 128, 0.8)' 
    ];
    return colors[index % colors.length];
    }

    function createAberturaEncerramentoChart(data) {
        const ctx = document.getElementById('abertura-encerramento-chart').getContext('2d');
        const labels = data.map(item => item.ANOMES_REF);
        const aberturas = data.map(item => item.ABERTURAS);
        const encerramentos = data.map(item => item.ENCERRADOS);
        const porcentagemEncerramento = data.map(item => item["% Aberturas x Encerrados"]);

        if (chartInstances.aberturaEncerramento) {
            chartInstances.aberturaEncerramento.destroy();
        }

        chartInstances.aberturaEncerramento = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Aberturas',
                        data: aberturas,
                        backgroundColor: 'rgba(0, 63, 92, 0.6)',
                        borderColor: 'rgba(0, 63, 92, 1)',
                        borderWidth: 1
                    },
                    {
                        label: 'Encerramentos',
                        data: encerramentos,
                        backgroundColor: 'rgba(188, 80, 144, 0.6)',
                        borderColor: 'rgba(188, 80, 144, 1)',
                        borderWidth: 1
                    },
                    {
                        label: '% Encerramentos',
                        data: porcentagemEncerramento,
                        type: 'line',
                        borderColor: 'rgba(255, 166, 0, 1)',
                        backgroundColor: 'rgba(255, 166, 0, 0.2)',
                        yAxisID: 'y1',
                        fill: true,
                        tension: 0.4
                    }
                ]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        position: 'left',
                        title: {
                            display: true,
                            text: 'Quantidade'
                        }
                    },
                    y1: {
                        beginAtZero: true,
                        position: 'right',
                        grid: {
                            drawOnChartArea: false
                        },
                        title: {
                            display: true,
                            text: 'Porcentagem (%)'
                        }
                    }
                },
                plugins: {
                    title: {
                        display: true,
                        text: 'Aberturas x Encerramento'
                    },
                    legend: {
                        position: 'top'
                    },
                    datalabels: {
                        anchor: 'end',
                        align: 'top',
                        color: 'rgba(0, 0, 0, 0.6)',
                        font: {
                            weight: 'bold'
                        },
                        formatter: (value, context) => {
                            if (context.datasetIndex === 0 || context.datasetIndex === 1) {
                                return value;
                            }
                            return '';
                        }
                    }
                }
            },
            plugins: [ChartDataLabels]
        });
    }

    function createEncerradosComplexidadeChart(data) {
        const ctx = document.getElementById('encerrados-complexidade-chart').getContext('2d');
        const labels = data.map(item => item.ANOMES_REF);
        const n1 = data.map(item => item.N1);
        const n2 = data.map(item => item.N2);
        const n3 = data.map(item => item.N3);

        if (chartInstances.encerradosComplexidade) {
            chartInstances.encerradosComplexidade.destroy();
        }

        chartInstances.encerradosComplexidade = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'N1',
                        data: n1,
                        borderColor: getColorForComplexidade('N1', true),
                        backgroundColor: getColorForComplexidade('N1', false),
                        fill: false,
                        tension: 0.4
                    },
                    {
                        label: 'N2',
                        data: n2,
                        borderColor: getColorForComplexidade('N2', true),
                        backgroundColor: getColorForComplexidade('N2', false),
                        fill: false,
                        tension: 0.4
                    },
                    {
                        label: 'N3',
                        data: n3,
                        borderColor: getColorForComplexidade('N3', true),
                        backgroundColor: getColorForComplexidade('N3', false),
                        fill: false,
                        tension: 0.4
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Encerrados x Complexidade'
                    },
                    legend: {
                        position: 'top'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Quantidade'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Período (ANOMES_REF)'
                        }
                    }
                }
            }
        });
    }

    function createLeadTimeTable(data) {
    const tableContainer = document.getElementById('leadtime-table');
    const months = data.map(item => item.ANOMES_REF);
    const leadTimes = ['D0', 'D1', 'D2', 'D3', 'D4', 'D5+'];

    let maxValue = 0;
    data.forEach(item => {
        leadTimes.forEach(leadTime => {
            if (item[leadTime] > maxValue) {
                maxValue = item[leadTime];
            }
        });
    });

    let tableHTML = '<div class="table-responsive"><table class="table table-bordered leadtime-table">';
    tableHTML += '<thead class="thead-dark"><tr><th></th>';

    months.forEach(month => {
        tableHTML += `<th>${month}</th>`;
    });

    tableHTML += '<th>Total</th>';
    tableHTML += '<th>Média</th>';
    tableHTML += '</tr></thead><tbody>';

    leadTimes.forEach(leadTime => {
        let total = 0;
        let count = 0;
        
        tableHTML += `<tr><td>${leadTime}</td>`;
        
        months.forEach(month => {
            const monthData = data.find(item => item.ANOMES_REF === month);
            const value = monthData ? monthData[leadTime] : 0;
            total += value;
            if (value > 0) count++;
            
            const backgroundColor = getColorForValue(value, maxValue);
            tableHTML += `<td style="background-color: ${backgroundColor}; color: black;">${value}</td>`;
        });

        const media = count > 0 ? (total / count).toFixed(1) : 0;
        tableHTML += `<td>${total}</td>`;
        tableHTML += `<td>${media}</td>`;
        tableHTML += '</tr>';
    });

    tableHTML += '</table></div>';
    tableContainer.innerHTML = tableHTML;
}

    function getColorForValue(value, maxValue) {
    const hue = ((1 - value / maxValue) * 120).toString(10);
    return `hsla(${hue}, 70%, 45%, 0.6)`;
    }

    loadJSONData(dataFiles).then(data => {
        cuboData = data;
        updateFilters();
        createCharts(cuboData);

        document.querySelectorAll('select').forEach(select => {
            select.addEventListener('change', () => {
                const filteredData = applyFilters(cuboData);
                createCharts(filteredData);
            });
        });
    });

    $('#filters-collapse').on('shown.bs.collapse', function () {
        $('#toggle-filters-btn').html('<i class="fas fa-eye-slash"></i> Ocultar Filtros');
    });

    $('#filters-collapse').on('hidden.bs.collapse', function () {
        $('#toggle-filters-btn').html('<i class="fas fa-eye"></i> Mostrar Filtros');
    });
});
