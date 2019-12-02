'use strict';

const puppeteer = require('puppeteer');
//const fs = require('fs');
const http = require('http');
const XLSX = require('xlsx');
const shell = require('shelljs');
const config = {
    codigo: "",
    inscricao: "",
    mes: "",
    ano: "",
    filename: "",
    debug: false,
    log: ""
}

if (process.argv.length < 5) {
    console.log("Contagem de parâmetros incorretas para o comando.");
    console.log("");
    console.log("Uso:");
    console.log("    node malha.js [codigo] [mes] [ano]");
    console.log("");
    console.log("Parâmetros:");
    console.log("    codigo = Código da empresa");
    console.log("    mes    = Mês de referencia da consulta");
    console.log("    ano    = Ano de referência da consulta");
    console.log("");
    console.log("Exemplo:");
    console.log("    node malha.js 615 01 2018");
} else {
    process.argv.forEach(function (val, index, array) {
        if (index == 2) {
            config.codigo = val;
            config.filename = config.codigo + "-" + config.ano + "-" + config.mes;
        } else if (index == 3) {
            config.mes = val;
            config.filename = config.codigo + "-" + config.ano + "-" + config.mes;
        } else if (index == 4) {
            config.ano = val;
            config.filename = config.codigo + "-" + config.ano + "-" + config.mes;
        } else if (index == 5 && val == "debug") {
            config.debug = true;
        } else if (index == 5) {
            config.log = val;
        }
    });

    let _ie_command = "python3 " + __dirname + "\\ConsultarIE.py " + config.codigo;
    console.log("Consultando IE");
    console.log("    " + _ie_command);
    let _ie = shell.exec(_ie_command).stdout

    // //config.inscricao = data;
    // //console.log("Empresa " + config.codigo + "  IE:" + data);
    config.inscricao = _ie;
    console.log("Empresa " + config.codigo + "  IE:" + config.inscricao);
    /*****************************************************************************************/
    (async () => {
        var wait2 = async function () {
            var _waiting = await page2.evaluate(() => window.getComputedStyle(document.querySelector("#j_idt7")).visibility);
            var _step = 1;
            while (_waiting == "visible") {
                await page2.waitFor(100);
                _waiting = await page2.evaluate(() => window.getComputedStyle(document.querySelector("#j_idt7")).visibility);
            }
        }
        var wait3 = async function () {
            var _waiting = await page2.evaluate(() => window.getComputedStyle(document.querySelector("#j_idt11")).visibility);
            var _step = 1;
            while (_waiting == "visible") {
                await page2.waitFor(100);
                _waiting = await page2.evaluate(() => window.getComputedStyle(document.querySelector("#j_idt11")).visibility);
            }
        }
        //aqui
        console.log("Iniciando o Chromium");
        const browser = await puppeteer.launch({
            headless: !(config.debug)
        });
        //const browser = await puppeteer.launch({headless: false});
        console.log("Abrindo abas para as consultas");
        const page = await browser.newPage();
        const page2 = await browser.newPage();
        var _selector = "";

        console.log("Configurando ambiente de download");
        await page2._client.send('Page.setDownloadBehavior', {
            behavior: 'allow',
            downloadPath: 'C:\\inetpub\\summa\\malhatemp'
        });
        const fs = require('fs');

        try {
            console.log("Indo para a página inicial do portal da malha");
            await page.goto('http://serv01.sefaz.go.gov.br/portalsefaz/portal.jsp');
            await page.screenshot({
                path: 'C:\\inetpub\\summa\\malhatemp\\passo_01.png'
            });

            console.log("Logando no sistema");
            await page.type('#txtUsuario', '6455425');
            await page.type('#txtSenha', '7347038413');
            await page.screenshot({
                path: 'C:\\inetpub\\summa\\malhatemp\\passo_02.png'
            });
            await page.click("input[name=Ok]");

            console.log("Aguardando o menu inicial");
            await page.waitForSelector("#caixaConteudoListagemSistemasItemDescricao");
            await page.screenshot({
                path: 'C:\\inetpub\\summa\\malhatemp\\passo_03.png'
            });

            console.log("Clicando na opção para Malha Fina Estadual");
            const newlink = await page.evaluate(() => document.querySelector('[title="Malha Fina Estadual"]').getAttribute("href"));
            await page2.goto(newlink);
            console.log("    " + newlink);
            
            await page2.screenshot({
                path: 'C:\\inetpub\\summa\\malhatemp\\passo_04.png'
            });
            //await page2.goto("http://serv01.sefaz.go.gov.br/smw/web/listarCriticasMes/listarCriticasMesContribuinte.jsf?param=N");
            await page2.goto("https://sistemas.sefaz.go.gov.br/smw/web/listarCriticasMes/listarCriticasMesContribuinte.jsf?param=N");
            await page2.screenshot({
                path: 'C:\\inetpub\\summa\\malhatemp\\passo_05.png'
            });

            var _wfl = true;
            while (_wfl) {
                console.log("    Esperando a tela de consulta")
                _wfl = await page2.evaluate(async () => {
                    let _e = document.querySelector("#campoInicio");
                    return _e == null || _e == "undefined";
                });
                if (_wfl) {
                    await page2.goto("https://sistemas.sefaz.go.gov.br/smw/web/listarCriticasMes/listarCriticasMesContribuinte.jsf?param=N");
                    await page2.screenshot({
                        path: 'C:\\inetpub\\summa\\malhatemp\\passo_05.png'
                    });
                }
            }

            console.log("Informando o periodo e a IE da empresa");
            console.log("    " + config.mes + "/" + config.ano);
            await page2.evaluate((config) => {
                document.querySelector("#campoInicio").value = config.mes + "/" + config.ano
            }, config);
            console.log("    " + config.inscricao);
            await page2.evaluate((config) => {
                document.querySelector("#campoInscricao").value = config.inscricao
            }, config);
            await page2.screenshot({
                path: 'C:\\inetpub\\summa\\malhatemp\\passo_06.png'
            });

            console.log("Clicando no botão de consulta");
            await page2.evaluate(() => document.querySelector("#j_idt47").click());
            await page2.screenshot({
                path: 'C:\\inetpub\\summa\\malhatemp\\passo_07.png'
            });

            await wait2();
            await page2.screenshot({
                path: 'C:\\inetpub\\summa\\malhatemp\\passo_08.png'
            });


            console.log("Verificando o status do processamento");
            var _status125 = "none"
            while (_status125 === "none") {
                _status125 = await page2.evaluate(async () => {
                    var _e = document.querySelectorAll("#dtArquivoProcessado_data > tr > td");
                    if (_e.length >= 10) {
                        _e = _e[9].querySelectorAll("div");
                        if (_e.length > 0) {
                            return _e[0].innerText;
                        }
                    }
                    return "";
                });
                await page2.waitFor(200);
            }
            console.log("    " + _status125);

            if (_status125 === "Nenhum arquivo entregue para este mês" || _status125 === "Arquivo entregue e ainda não processado pelo Malha Fina" || _status125 === "Arquivo processado. Nenhuma crítica encontrada") {
                console.log("Sem críticas. Criando arquivo de notificação.")
                var _filedata = {
                    mensagem: _status125,
                    entradas: null,
                    saidas: null
                }
                var _text = JSON.stringify(_filedata)
                fs.writeFile("C:\\inetpub\\summa\\malhanew\\" + config.filename + ".json", _text, function (err) {
                    if (err) {
                        return console.log(err);
                    }
                });
            } else {
                var _principal = page2.frames("principal")[0];
                var _alerta = "";
                await wait2();
                await wait2();

                console.log("Procurando o botão para expandir os detalhes da malha");
                _selector = "#dtArquivoProcessado\\:0\\:j_idt92";
                var _button = await _principal.$(_selector);
                while (_button == null) {
                    _button = await _principal.$(_selector);
                    console.log("    Waiting for \"" + _selector + "\"")
                    _alerta = await page2.evaluate(async () => {
                        var _e = document.querySelectorAll(".ui-growl-title");
                        if (_e.length > 0) {
                            return _e[0].innerText;
                        } else {
                            _e = document.querySelectorAll("#dtArquivoProcessado_data > tr > td > .ui-dt-c");
                            if (_e.length == 10) {
                                return _e[9].innerText;
                            }
                        }
                        return "";
                    });
                    if (_alerta != "") {
                        console.log("Sem malha, encontrado um alerta:");
                        console.log("    - " + _alerta);
                        break;
                    }
                }

                if (_alerta == "") {
                    console.log("Botão encontrado, abrindo a malha");
                    _button.click();
                    await wait2();
                    await page2.waitFor(1000);

                    console.log("Verificando a quantidade de operações");
                    let _rows235 = await page2.evaluate(async () => {
                        let _r = [];
                        let _e = document.querySelectorAll("#dtArquivoProcessado\\:0\\:dtProcessamentos_data > tr");

                        for (let i = 0; i < _e.length; i++) {
                            let _ci = {
                                download: _e[i].querySelectorAll("td")[0].querySelectorAll(".ui-commandlink").length > 0,
                                nome: _e[i].querySelectorAll("td")[1].innerText.trim(),
                                quant: parseInt(_e[i].querySelectorAll("td")[2].innerText.trim())
                            }
                            _r.push(_ci);
                        }

                        return _r;
                    });
                    if (_rows235.length > 1) {
                        console.log("    " + _rows235.length + " registros encontrados:");
                    } else {
                        console.log("    " + _rows235.length + " registro encontrado:");
                    }
                    for (let i = 0; i < _rows235.length; i++) {
                        console.log("        " + _rows235[i].nome);
                    }

                    var processarOperacoes = async function (options) {
                        console.log("");
                        const fs = require('fs');

                        if (_rows235[options.index].download) {
                            var _nome = _rows235[options.index].nome;
                            var _tipo = _nome.toLowerCase().indexOf("saída") > -1 || _nome.toLowerCase().indexOf("saida") > -1 ? "S" : "E";
                            console.log("Verificando as " + (_tipo == "S" ? "Saídas" : "Entradas"));

                            console.log("Expandindo a " + _rows235[options.index].nome.replace("Proc. ", ""));
                            let _selector235 = "#dtArquivoProcessado\\:0\\:dtProcessamentos\\:" + options.index + "\\:j_idt115";
                            var _button235 = await _principal.$(_selector235);
                            await page2.waitFor(500);
                            if (_button235 != null) {
                                _button235.click();
                            }
                            await page2.waitFor(1000);

                            console.log("Verificando se a operação possui registro C100");
                            let _registros235 = await page2.evaluate(async (_dindex) => {
                                let _e = document.querySelectorAll("#dtArquivoProcessado\\:0\\:dtProcessamentos\\:" + _dindex + "\\:dtCriticasPorTipo_data");
                                return _e[0].querySelectorAll("td")[1].innerText.trim();
                            }, options.index);
                            if (_registros235 === "Arquivo EFD sem registros C100") {
                                console.log("    " + _registros235);
                            } else {
                                console.log("Procurando e clicando no botão de tipo de download");
                                let _clicarBotaoTipoDownload = async function (_dindex) {
                                    var _buttonpreD = await _principal.$("#dtArquivoProcessado\\:0\\:dtProcessamentos\\:" + _dindex + "\\:expButton");
                                    while (_buttonpreD == null) {
                                        console.log("    Esperando o botão de tipo de download");
                                        _buttonpreD = await _principal.$("#dtArquivoProcessado\\:0\\:dtProcessamentos\\:" + _dindex + "\\:expButton");
                                    }
                                    _buttonpreD.click();
                                }
                                await _clicarBotaoTipoDownload(options.index);

                                var _subPDownCounter = 0;
                                var _subPDown = "";
                                while (_subPDown !== "block") {
                                    console.log("    Esperando a janela com os tipos de download")
                                    _subPDown = await page2.evaluate(async (_dindex) => {
                                        let _e = document.querySelectorAll("#dtArquivoProcessado\\:0\\:dtProcessamentos\\:" + _dindex + "\\:j_idt128");
                                        return _e[0].style.display;
                                    }, options.index);
                                    if (_subPDownCounter > 20) {
                                        console.log("Procurando e clicando no botão de tipo de download novamente")
                                        _subPDownCounter = 0;
                                        _clicarBotaoTipoDownload(options.index);
                                    } else {
                                        _subPDownCounter += 1;
                                    }
                                }

                                var _clicarDownload = async function () {
                                    console.log("Procurando e clicando no botão de download em formato planilha");
                                    var _excelDownCounter = 0;
                                    var _clicarBotaoDownloadExcel = async function (page123, _dindex) {
                                        await page123.evaluate(async (_dindex) => {
                                            let _e = document.querySelectorAll("#dtArquivoProcessado\\:0\\:dtProcessamentos\\:" + _dindex + "\\:j_idt130");
                                            _e[0].click();
                                        }, _dindex);
                                    }
                                    await _clicarBotaoDownloadExcel(page2, options.index);

                                    var _wait = function (ms) {
                                        return new Promise(resolve => setTimeout(resolve, ms));
                                    }
                                    await _wait(2000);

                                    while (!fs.existsSync('C:\\inetpub\\summa\\malhatemp\\RelatorioCriticas.xls')) {
                                        console.log("    Esperando o download do arquivo...");
                                        if (_excelDownCounter > 20) {
                                            console.log("Procurando e clicando no botão de download em formato planilha novamente")
                                            _excelDownCounter = 0;
                                            await _clicarBotaoDownloadExcel(page2, options.index);
                                        } else {
                                            _excelDownCounter += 1;
                                        }
                                    }

                                    console.log("Renomeando arquivo baixado")
                                    fs.rename('C:\\inetpub\\summa\\malhatemp\\RelatorioCriticas.xls', 'C:\\inetpub\\summa\\malhatemp\\' + config.filename + '-' + _tipo + '.xls', function (err) {
                                        if (err) console.log('ERROR: ' + err);
                                    });

                                    console.log("Fazendo backup de segurança do arquivo.");
                                }

                                var _eepath = 'C:\\inetpub\\summa\\malhatemp\\' + config.filename + '-' + _tipo + '.xls';

                                var _processarExcel = function () {
                                    console.log("Processando arquivo baixado")
                                    console.log("   Arquivo=" + _eepath);
                                    const workbook = XLSX.readFile(_eepath);
                                    const sheet_name_list = workbook.SheetNames;
                                    for (var i = 0; i < sheet_name_list.length; i++) {
                                        console.log("       Pagina=" + sheet_name_list[i]);
                                        var _sheet = XLSX.utils.sheet_to_json(workbook.Sheets[sheet_name_list[i]]);
                                        
                                        var _row2 = _sheet[1];
                                        var _descricao = "";
                                        for (var key2 in _row2) {
                                            _descricao = key2;
                                            if(_descricao == "NFE escriturada status dif"){
                                                _descricao = "NFE escriturada status diferente";
                                            } else {
                                                _descricao = key2
                                            }
                                            break;
                                        }

                                        var _e = {
                                            descricao: _descricao, /*sheet_name_list[i],*/
                                            notas: []
                                        };
                                        for (var r = 1; r < _sheet.length; r++) {
                                            var _row = _sheet[r];
                                            var _serie = "";
                                            for (var key in _row) {
                                                _serie = _row[key];
                                                break;
                                            }
                                            var _d = {
                                                serie: _serie,
                                                numero: _row["__EMPTY"],
                                                cancelado: _row["__EMPTY_1"],
                                                valor: _row["__EMPTY_2"],
                                                cnpj: _row["__EMPTY_3"],
                                                processamento: _row["__EMPTY_4"],
                                                chave: _row["__EMPTY_5"],
                                            };
                                            _e.notas.push(_d);
                                        }
                                        if (_tipo == "S") {
                                            _opcoes_processamento.mapa.saidas.notas.push(_e);
                                        } else {
                                            _opcoes_processamento.mapa.entradas.notas.push(_e);
                                        }
                                    }
                                }

                                await _clicarDownload();

                                if (fs.existsSync(_eepath)) {
                                    _processarExcel();
                                } else {
                                    console.log("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
                                    console.log("        ARQUIVO NÃO ENCONTRADO");
                                    console.log("           Tentando novamente")
                                    console.log("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");

                                    await _clicarDownload();

                                    if (fs.existsSync(_eepath)) {
                                        _processarExcel();
                                    } else {
                                        console.log("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
                                        console.log("        ARQUIVO NÃO ENCONTRADO");
                                        console.log("           Tentando novamente")
                                        console.log("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");

                                        await _clicarDownload();
                                    }

                                    if (fs.existsSync(_eepath)) {
                                        _processarExcel();
                                    } else {
                                        console.log("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
                                        console.log("        ARQUIVO NÃO ENCONTRADO");
                                        console.log("              Verificar")
                                        console.log("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
                                    }
                                }
                            }
                        } else {
                            if (_rows235[options.index].quant > 0) {
                                console.log("             ERRO!");
                                console.log("Erro! Verificar empresa " + config.codigo + " IE " + config.inscricao);
                                console.log("ela possui crítica mas não possui botão de expansão de operação");
                            } else {
                                console.log(_rows235[options.index].nome.replace("Proc. ", "") + " com 0 críticas");
                            }
                        }
                    }

                    var _opcoes_processamento = {
                        index: 0,
                        mapa: {
                            inscricao: config.inscricao,
                            mensagem: "",
                            entradas: {
                                mensagem: "",
                                notas: []
                            },
                            saidas: {
                                mensagem: "",
                                notas: []
                            }
                        }
                    }
                    await processarOperacoes(_opcoes_processamento);
                    while (fs.existsSync('C:\\inetpub\\summa\\malhatemp\\RelatorioCriticas.xls')) {
                        fs.unlink('C:\\inetpub\\summa\\malhatemp\\RelatorioCriticas.xls');
                    };
                    _opcoes_processamento.index = 1;
                    await processarOperacoes(_opcoes_processamento);

                    console.log("");
                    console.log("Convertendo as informações da Malha para JSON");
                    var _text = JSON.stringify(_opcoes_processamento.mapa);
                    //var fs = require('fs');
                    var _mp = "C:\\inetpub\\summa\\malhanew\\" + config.filename + ".json";
                    console.log("Salvando malha para " + _mp);
                    fs.writeFile(_mp, _text, function (err) {
                        if (err) {
                            return console.log(err);
                        }
                    });
                    console.log("Consulta da malha finalizada (1)!");
                } else {
                    console.log("Gerando arquivo de consolidação com o alerta");
                    var _filedata = {
                        inscricao: config.inscricao,
                        mensagem: _alerta,
                        entradas: {},
                        saidas: {}
                    };
                    var _text = JSON.stringify(_filedata);
                    var _mp = "C:\\inetpub\\summa\\malhanew\\" + config.filename + ".json";
                    console.log("Salvando malha para " + _mp);
                    fs.writeFile(_mp, _text, function (err) {
                        if (err) {
                            return console.log(err);
                        }
                    });
                    console.log("Consulta da malha finalizada (2)!");
                }
            }
            /******************************************************************************************/
        } catch (e) {
            console.log("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
            console.log("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
            console.log(e);
            console.log("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
            console.log("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
            await browser.close();
            process.exit(9)
        } finally {
            await browser.close();
            process.exit(0)
        }
    })();
}
console.log("Was hereeeee 4 ?!?");