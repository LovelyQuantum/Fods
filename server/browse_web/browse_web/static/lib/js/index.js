$(document).ready(function () {
    var currentDevice = "";
    var selectDevice = "";
    $(".sub").click(function (event) {
        var deviceId;
        if ($(event.target)[0].id != "") {
            deviceId = $(event.target)[0].id
        } else {
            deviceId = $(event.target).context.children[0].id
        }
        if (deviceId.indexOf('Look') != -1) {
            var chartTitle = $("#" + deviceId).parents(".sub-menu").children("a").children("span").html();
            $("#chartTitle").html(chartTitle + "最近30天发生预警次数")
            var tem = deviceId.replace("Look", "");
            var img = $("#" + tem).children("div").children("canvas");
            $(".mt").hide()
            $(".block").hide();
            $(".block").attr("class", "col-md-12 col-sm-12 mb block");
            getCharts(tem);
            $("#midDisplay").attr("class", "row col-lg-9");
            imageToTable();
            var deviceId = {"deviceId": tem.replace("device","")};
            var imgId = Math.ceil(deviceId.deviceId/3);
            console.log(imgId)
            $(".midImage").attr("height", "37%");
            img.attr("width", "100%");
            img.attr("height", "80%");
            $("#" + tem).attr("class", "col-md-12 col-sm-12 mb block");

            // $("#serverstatus"+deviceId.deviceId).attr("src", "/camera_feed/" + deviceId.deviceId + "/1");
            $("#" + tem).show();
            $("#allDevice").show();
            $("#rightSide").show();
        } else if (deviceId.indexOf('Set') != -1) {
            selectDevice = deviceId.replace("Set", "");
            $("#loginTitle").val("set")
            // $.ajax({
            //     url: '/is_login',
            //     type: 'post',
            //     data: '',
            //     dataType: 'json',
            //     success: function (data) {
            //         if (data.boo === true) {
                        getSetTableInfo(deviceId);
                        $(".mt").hide();
                        $("#set").show();
                        $("#midDisplay").attr("class", "row col-lg-12");
                        $("#rightSide").hide();
            //         } else {
            //             $("#exampleModal2").modal('show')
            //             $("#loginTitle").val(deviceId)
            //         }
            //     }
            // });

        }
    })
    $.ajax({
        url: '/is_login',
        type: 'post',
        data: '',
        dataType: 'json',
        success: function (data) {
            if (data.boo === true) {
                $(".pull-right").show();
            }
        }
    })

    //左侧边栏获取所有设备
    $("#lookAll").click(function () {
        imageToTable();
        $("#midDisplay").attr("class", "row col-lg-9");
        $(".mt").hide();
        $(".midImage").attr("height", "37%");
        $(".block").attr("class", "col-md-4 col-sm-4 mb block");
        $(".block").show();
        $("#allDevice").show();
        $("#rightSide").show();
        currentDevice = "";
        openFullScreen();
    })

    //登陆
    $("#login").click(function () {
        var json = {"username": $("#account").val(), "password": $("#pd").val()};

        var loginTitle = $("#loginTitle").val();
        $.ajax({
            url: '/login',
            type: 'post',
            data: json,
            dataType: 'json',
            success: function (data) {
                if (data.boo === true) {
                    $("#exampleModal2").modal('hide')
                    if (loginTitle.indexOf('Set') != -1) {
                        getSetTableInfo(loginTitle.replace("Set", ""));
                        $(".mt").hide();
                        $("#set").show();
                        $("#midDisplay").attr("class", "row col-lg-12");
                        $("#rightSide").hide();
                    } else if (loginTitle.indexOf('Exercise') != -1) {
                        var json = {'temp_page': 1, 'dataset_page': 1};
                        $.ajax({
                            url: '/getPhotos',
                            type: 'post',
                            data: json,
                            dataType: 'json',
                            success: function (data) {
                                if (data.boo === true) {
                                    $(".mt").hide();
                                    tableToImage()
                                    $("#draw").show();
                                    setMidImage(data.temp);
                                    initPage(data.temp_maxpage, "imagePage");
                                    setHistoryTable(data.dataset);
                                    initPage(data.dataset_maxpage, "asidePage")
                                }
                            }
                        })
                    }

                } else {
                    alert("登陆失败")
                }
            }
        })
    });


    var initExercise = function () {
        var json = {'temp_page': 1, 'dataset_page': 1};
        $.ajax({
            url: '/getPhotos',
            type: 'post',
            data: json,
            dataType: 'json',
            success: function (data) {
                if (data.boo === true) {
                    $(".mt").hide();
                    setMidImage(data.temp);
                    initPage(data.temp_maxpage, "imagePage");
                    setHistoryTable(data.dataset);
                    initPage(data.dataset_maxpage, "asidePage");
                    tableToImage();
                    $("#draw").show();
                } else {
                    $("#exampleModal2").modal('show');
                }
            }
        })
    };


    $("#deviceExercise").click(function () {
        $("#loginTitle").val("Exercise");

        $.ajax({
            url: '/checkStatus',
            type: 'post',
            data: '',
            dataType: 'json',
            success: function (data) {
                if (data.boo === true) {

                    initExercise();

                    var html = "";
                    $.each(data.classes, function (n, value) {
                        html += "<li id=\"tag" + n + "\" class=\"selectDrop\"><a>" + value + "</a></li>"
                    })
                    $("#classes").html(html);

                } else {
                    alert("系统正在训练中，暂时不能进行此操作")
                }
            }
        })
        // $.ajax({
        //     url: '/getPhotos',
        //     type: 'post',
        //     data: json,
        //     dataType: 'json',
        //     success: function (data) {
        //         if (data.boo === true) {
        //             $(".mt").hide();
        //             tableToImage()
        //             $("#draw").show();
        //             setMidImage(data.temp);
        //             initPage(data.temp_maxpage, "imagePage");
        //             setHistoryTable(data.dataset);
        //             initPage(data.dataset_maxpage, "asidePage");
        //             classes = data.classes;
        //             var html = "";
        //             $.each(classes, function (n, value) {
        //                 // FIXME 修正
        //                 html += "<li id=\"" + value.get(n) + "\"><a>" + value.get + "</a></li>"
        //             })
        //             $("#classes").html(html);
        //         } else {
        //             $("#exampleModal2").modal('show')
        //         }
        //
        //     }
        // })
    });

    $("#uploadImage").click(function () {
        $.ajax({
            url: '/checkExist',
            type: 'post',
            data: '',
            dataType: 'json',
            success: function (data) {
                if (data.boo === true) {
                    $(".mt").hide();
                    $("#upload").show();
                    $("#midDisplay").attr("class", "row col-lg-12");
                    $("#rightSide").hide();
                } else {
                    alert("请先完成当前图片处理")
                }
            }
        })
    })

    //上传完成后请求图片列表
    $("#Done").click(function () {
        var json = {'temp_page': 1, 'dataset_page': 1};
        $.ajax({
            url: '/getPhotos',
            type: 'post',
            data: json,
            dataType: 'json',
            success: function (data) {
                if (data.boo === true) {
                    $(".mt").hide();
                    tableToImage()
                    $("#draw").show();
                    setMidImage(data.temp);
                    initPage(data.temp_maxpage, "imagePage");
                    setHistoryTable(data.dataset);
                    initPage(data.dataset_maxpage, "asidePage")
                }
            }
        })

    })


    var tableToImage = function () {
        $(".ds").hide();
        $("#midDisplay").attr("class", "row col-lg-7");
        $("#rightSide").attr("class", "row col-lg-5");
        $("#rightSide").show();
        $("#showImage").show();
    }

    var imageToTable = function () {
        $(".ds").hide();
        $("#rightSide").attr("class", "row col-lg-3");
        $("#showImage").hide();
        $("#tableGraph").show();
    }


    //左侧边栏获取所有设备
    $("#lookAll").click(function () {
        imageToTable();
        $("#midDisplay").attr("class", "row col-lg-9");
        $(".mt").hide();
        $(".midImage").attr("height", "37%");
        $(".block").attr("class", "col-md-12 col-sm-12 mb block");
        $(".block").show();
        $("#allDevice").show();
        $("#rightSide").show();
        currentDevice = "";
        openFullScreen();
    })


    //配置界面中获得表单
    var getSetTableInfo = function (deviceId) {
        var json = {"deviceId": deviceId};
        $.ajax({
            url: '/getDevice',
            type: 'post',
            data: json,
            dataType: 'json',
            success: function (data) {
                $("#camera_id").val(deviceId.replace("Set", "").replace("device", ""));
                $("#name").val(data.name);
                $("#ip").val(data.ip);
                $("#username").val(data.username);
                $("#password").val(data.password);
                $("#client").val(data.client);
                $("#mode").val(data.mode);
                $("#network").val(data.network_id);
                $("#start_point").val(data.start_point);
                $("#nor_lim").val(data.nor_lim);
                $("#ext_lim").val(data.ext_lim);
                $("#borderline").val(data.borderline)
            },
            error: function () {

            }
        })
    }


    //设置中的画图
    var paint = {
        init: function () {
            this.load();
        },
        load: function () {
            this.x = [];//记录鼠标移动是的X坐标
            this.y = [];//记录鼠标移动是的Y坐标
            this.maxX = 0;
            this.maxY = 0;
            this.minX = 123123123;
            this.minY = 123123123;
            this.rectWidth = 0;
            this.rectHeight = 0;
            this.coordinate = [];
            this.clickDrag = [];
            this.img = new Image;
            this.lock = false;//鼠标移动前，推断鼠标是否按下
            this.drawType = false;  //false表示画路径，true表示画直线
            this.let;
            this.storageColor = "#FF0000";
            this.fontWeight = [2, 5, 8];
            this.$ = function (id) {
                return typeof id == "string" ? document.getElementById(id) : id;
            },
                this.canvas = this.$("canvas");
            if (!this.canvas.getContext) {
                alert("您的浏览器不支持 canvas 标签");
                return;
            }
            this.cxt = this.canvas.getContext('2d');
            this.cxt.lineJoin = "round";//context.lineJoin - 指定两条线段的连接方式
            this.cxt.lineWidth = 1;//线条的宽度
            this.cxt.strokeStyle = "#FF0000";
            this.iptClear = this.$("clear");
            this.w = this.canvas.width;//取画布的宽
            this.h = this.canvas.height;//取画布的高
            this.touch = ("createTouch" in document);//判定是否为手持设备
            this.StartEvent = this.touch ? "touchstart" : "mousedown";//支持触摸式使用相应的事件替代
            this.MoveEvent = this.touch ? "touchmove" : "mousemove";
            this.EndEvent = this.touch ? "touchend" : "mouseup";
            this.bind();
        },
        bind: function () {
            var t = this;
            /*清除画布*/
            this.iptClear.onclick = function () {
                t.coordinate = [];
                t.clear();
                t.cxt.drawImage(t.img, 0, 0);
            };
            /*鼠标按下事件，记录鼠标位置。并绘制，解锁lock，打开mousemove事件*/
            this.canvas['on' + t.StartEvent] = function (e) {
                var touch = t.touch ? e.touches[0] : e;
                var _x = touch.pageX - $("#canvas").offset().left  //touch.target.offsetLeft;//鼠标在画布上的x坐标，以画布左上角为起点
                var _y = touch.pageY - $("#canvas").offset().top   //touch.target.offsetTop;//鼠标在画布上的y坐标，以画布左上角为起点
                if (t.drawType == false && t.coordinate.length > 0) {
                    t.rectWidth = _x - (t.coordinate[t.coordinate.length - 1].minX);
                    t.rectHeight = _y - (t.coordinate[t.coordinate.length - 1].minY);
                }
                t.movePoint(_x, _y);//记录鼠标位置
                t.drawPoint();//绘制路线
                t.lock = true;
            };
            /*鼠标移动事件*/
            this.canvas['on' + t.MoveEvent] = function (e) {
                e.stopPropagation();////////////////////////////////////////////////禁止冒泡事件/////////////////////////////////////////
                var touch = t.touch ? e.touches[0] : e;
                //t.lock为true则运行
                if (t.lock) {
                    var _x = touch.pageX - $("#canvas").offset().left //touch.target.offsetLeft;//鼠标在画布上的x坐标，以画布左上角为起点
                    var _y = touch.pageY - $("#canvas").offset().top //touch.target.offsetTop;//鼠标在画布上的y坐标。以画布左上角为起点
                    t.movePoint(_x, _y, true);//记录鼠标位置
                    t.drawPoint();//绘制路线
                }
            };
            this.canvas['on' + t.EndEvent] = function (e) {
                /*重置数据*/

                if (t.drawType == false && t.coordinate.length < 1) {
                    t.minX = t.minX - 208;
                    t.minY = t.minY - 208;
                    t.maxX = t.minX + 416;
                    t.maxY = t.minY + 416;
                    t.cxt.beginPath();
                    t.cxt.rect(t.minX, t.minY, 416, 416);
                    t.cxt.closePath();
                    t.cxt.stroke();
                    console.log("one")
                }
                var position = {"minX": t.minX, "minY": t.minY, "maxX": t.maxX, "maxY": t.maxY};
                t.coordinate.push(position);
                t.lock = false;
                t.x = [];
                t.y = [];
                t.maxX = 0;
                t.maxY = 0;
                t.minX = 123123123;
                t.minY = 123123123;
                t.clickDrag = [];
                // clearInterval(t.Timer);
                // t.Timer=null;
            };
        },
        //blind end
        movePoint: function (x, y, dragging) {
            /*将鼠标坐标加入到各自相应的数组里*/
            this.x.push(x);
            this.y.push(y);
            if (this.minX == 123123123) {
                this.minX = x;
                this.minY = y;
            } else {
                this.maxX = x;
                this.maxY = y;
            }
            this.clickDrag.push(y);
        },
        drawPoint: function (x, y, radius) {
            //循环数组
            if (this.drawType == false) {      //画路径
                for (var i = 0; i < this.x.length; i++) {
                    if (this.coordinate.length > 0) {
                        var index = this.coordinate[this.coordinate.length - 1];
                        if (this.x[0] >= index.minX && this.x[0] <= index.maxX && this.y[0] >= index.minY && this.y[0] <= index.maxY) {
                            this.cxt.beginPath();
                            if (i != this.length - 1) {
                                this.clear();
                                this.cxt.drawImage(this.img, 0, 0);
                            }
                            this.minX = this.x[i] - this.rectWidth;
                            this.minY = this.y[i] - this.rectHeight;
                            this.maxX = this.minX + 416;
                            this.maxY = this.minY + 416;
                            this.cxt.rect(this.minX, this.minY, 416, 416);
                            this.cxt.closePath();
                            this.cxt.stroke();
                        }
                    }
                }
            } else if (this.drawType == true) {     //画直线
                for (var i = 0; i < this.x.length; i++) {
                    if (this.coordinate.length < 2) {
                        this.cxt.beginPath();//context.beginPath() , 准备绘制一条路径
                        if (i != this.length - 1) {
                            this.clear();
                            this.cxt.drawImage(this.img, 0, 0);
                            if (this.coordinate.length != 0) {
                                this.cxt.moveTo(this.coordinate[0].minX, this.coordinate[0].minY);
                                this.cxt.lineTo(this.coordinate[0].maxX, this.coordinate[0].maxY);
                            }
                        }
                        this.cxt.moveTo(this.x[0], this.y[0]);
                        this.cxt.lineTo(this.x[i], this.y[i]);//context.lineTo(x, y) , 将当前点与指定的点用一条笔直的路径连接起来
                        this.cxt.closePath();//context.closePath() , 假设当前路径是打开的则关闭它
                        this.cxt.stroke();//context.stroke() , 绘制当前路径
                    }
                }
            }

        },
        clear: function () {
            this.cxt.clearRect(0, 0, this.w, this.h);//清除画布，左上角为起点
        },
        getCoordinate: function () {
            return this.coordinate;
        },
        drawRect: function () {
            for (var i = 0; i < this.coordinate.length; i++) {
                this.cxt.rect(this.coordinate[i].minX, this.coordinate[i].minY, this.coordinate[i].maxX - this.coordinate[i].minX, this.coordinate[i].maxY - this.coordinate[i].minY);
                this.cxt.stroke();
            }
        },
        setBackground: function (imgUrl) {
            this.clear();
            this.coordinate = [];
            this.img.src = imgUrl;
            this.cxt.drawImage(this.img, 0, 0);
        },
        maxMinXY: function (x, y) {
            this.maxX = this.maxX < x ? x : this.maxX;
            this.maxY = this.maxY < y ? y : this.maxY;
            this.minX = this.minX < x ? this.minX : x;
            this.minY = this.minY < y ? this.minY : y;
        },
        setType: function (type) {
            this.drawType = type;
        }
    };


    //训练中的画图
    var paint2 = {
        init: function () {
            this.load();
        },
        load: function () {
            this.x = [];//记录鼠标移动是的X坐标
            this.y = [];//记录鼠标移动是的Y坐标
            this.maxX = 0;
            this.maxY = 0;
            this.minX = 123123123;
            this.minY = 123123123;
            this.coordinate = [];
            this.clickDrag = [];
            this.img = new Image;
            this.lock = false;//鼠标移动前，推断鼠标是否按下
            this.isEraser = false;
            this.storageColor = "#FF0000";
            this.fontWeight = [2, 5, 8];
            this.$ = function (id) {
                return typeof id == "string" ? document.getElementById(id) : id;
            },
                this.canvas = this.$("drawImage");
            if (!this.canvas.getContext) {
                alert("您的浏览器不支持 canvas 标签");
                return;
            }
            this.cxt = this.canvas.getContext('2d');
            this.cxt.lineJoin = "round";//context.lineJoin - 指定两条线段的连接方式
            this.cxt.lineWidth = 1;//线条的宽度
            this.cxt.strokeStyle = "#FF0000";
            this.iptClear = this.$("drawclear");
//	        this.revocation=this.$("revocation");
            this.w = this.canvas.width;//取画布的宽
            this.h = this.canvas.height;//取画布的高
            this.touch = ("createTouch" in document);//判定是否为手持设备
            this.StartEvent = this.touch ? "touchstart" : "mousedown";//支持触摸式使用相应的事件替代
            this.MoveEvent = this.touch ? "touchmove" : "mousemove";
            this.EndEvent = this.touch ? "touchend" : "mouseup";
            this.bind();
        },
        bind: function () {
            var t = this;
            /*清除画布*/
            this.iptClear.onclick = function () {
                t.clear();
                t.coordinate = [];
                t.cxt.drawImage(t.img, 0, 0);
            };
            /*鼠标按下事件，记录鼠标位置。并绘制，解锁lock，打开mousemove事件*/
            this.canvas['on' + t.StartEvent] = function (e) {
                var touch = t.touch ? e.touches[0] : e;
                var _x = touch.pageX - $("#drawImage").offset().left  //touch.target.offsetLeft;//鼠标在画布上的x坐标，以画布左上角为起点
                var _y = touch.pageY - $("#drawImage").offset().top   //touch.target.offsetTop;//鼠标在画布上的y坐标，以画布左上角为起点
                if (t.isEraser) {
                    t.resetEraser(_x, _y, touch);
                } else {
                    t.movePoint(_x, _y);//记录鼠标位置
                    t.drawPoint();//绘制路线
                }
                t.lock = true;
            };
            /*鼠标移动事件*/
            this.canvas['on' + t.MoveEvent] = function (e) {
                e.stopPropagation();////////////////////////////////////////////////禁止冒泡事件/////////////////////////////////////////
                var touch = t.touch ? e.touches[0] : e;
                //t.lock为true则运行
                if (t.lock) {
                    var _x = touch.pageX - $("#drawImage").offset().left //touch.target.offsetLeft;//鼠标在画布上的x坐标，以画布左上角为起点
                    var _y = touch.pageY - $("#drawImage").offset().top //touch.target.offsetTop;//鼠标在画布上的y坐标。以画布左上角为起点
                    if (t.isEraser) {
                        // t.rect(this.minX,this.minY,this.maxX,this.maxY);
                        //  t.stroke();
                        t.resetEraser(_x, _y, touch);
                    } else {
                        t.movePoint(_x, _y, true);//记录鼠标位置
                        t.drawPoint();//绘制路线
                    }
                }
            };
            this.canvas['on' + t.EndEvent] = function (e) {
                /*重置数据*/

                // t.cxt.rect(t.minX,t.minY,t.maxX-t.minX,t.maxY-t.minY);
                // t.cxt.stroke();
                var position = {"minX": t.minX, "minY": t.minY, "maxX": t.maxX, "maxY": t.maxY};
                t.coordinate.push(position);
                t.lock = false;
                t.x = [];
                t.y = [];
                t.maxX = 0;
                t.maxY = 0;
                t.minX = 123123123;
                t.minY = 123123123;
                t.clickDrag = [];
                clearInterval(t.Timer);
                t.Timer = null;
            };
        },
        //blind end
        movePoint: function (x, y, dragging) {
            /*将鼠标坐标加入到各自相应的数组里*/
            this.x.push(x);
            this.y.push(y);
            this.maxX = this.maxX < x ? x : this.maxX;
            this.maxY = this.maxY < y ? y : this.maxY;
            this.minX = this.minX < x ? this.minX : x;
            this.minY = this.minY < y ? this.minY : y;
            this.clickDrag.push(y);
        },
        drawPoint: function (x, y, radius) {
            //循环数组
            if (this.coordinate.length < 1) {
                for (var i = 0; i < this.x.length; i++) {
                    this.cxt.beginPath();//context.beginPath() , 准备绘制一条路径
                    if (this.clickDrag[i] && i) {//当是拖动并且i!=0时，从上一个点開始画线。
                        this.cxt.moveTo(this.x[i - 1], this.y[i - 1]);//context.moveTo(x, y) , 新开一个路径，并指定路径的起点
                    } else {
                        this.cxt.moveTo(this.x[i] - 1, this.y[i]);
                    }
                    this.cxt.lineTo(this.x[i], this.y[i]);//context.lineTo(x, y) , 将当前点与指定的点用一条笔直的路径连接起来
                    this.cxt.closePath();//context.closePath() , 假设当前路径是打开的则关闭它
                    this.cxt.stroke();//context.stroke() , 绘制当前路径
                    // this.cxt.rect(this.x[0],this.y[0],this.x[i]-this.x[0],this.y[i]-this.y[0]);
                    // this.cxt.stroke();
                }
            }
        },
        clear: function () {
            this.cxt.clearRect(0, 0, this.w, this.h);//清除画布，左上角为起点
        },
        getCoordinate: function () {
            return this.coordinate;
        },
        drawRect: function () {
            for (var i = 0; i < this.coordinate.length; i++) {
                this.cxt.rect(this.coordinate[i].minX, this.coordinate[i].minY, this.coordinate[i].maxX - this.coordinate[i].minX, this.coordinate[i].maxY - this.coordinate[i].minY);
                this.cxt.stroke();
            }
        },
        setBackground: function (imgUrl) {
            this.clear();
            this.coordinate = [];
            this.img.src = imgUrl;
            this.cxt.drawImage(this.img, 0, 0);
        },
        resetCanvas: function () {
            this.clear();
            this.coordinate = [];
            this.cxt.drawImage(this.img, 0, 0);
        }
    };


    (function () {
        paint.init();
        paint2.init();
    })();


    // 提交[{},{}]
    $("#save").click(function () {
        if (paint2.getCoordinate().length <= 0) {
            alert("请框选异物");
            return;
        }
        if ($("#dropdownMenu2").html().indexOf("异物类型") != -1) {
            alert("请选择异物类型");
            return;
        }
        var type = $(".type-dropwn").children("._active")[0].id;
        var imgId = $("#ImgId").val();
        var json = {"data": paint2.getCoordinate(), "imgId": imgId, "type": type};
        //
        paint2.resetCanvas();
        $.ajax({
            url: '/saveStep',
            type: 'post',
            data: json,
            dataType: 'json',
            success: function (data) {
                if (data.boo == true) {
                    alert("保存成功");
                    $("#exampleModal5").modal('hide');
                    var html = "";
                    $.each(data.list, function (n, value) {
                        html += "<div id=\"img\" class=\"col-md-2 col-sm-2 display-image tmpImg\">" +
                            "<div class=\"grey-panel pn donut-chart\">" +
                            "<img id=\"serverstatus1\" src=\"" + value.src + "\" width=\"100%\" alt=\"" + value.id + "\"/>" +
                            "</div>" +
                            "</div>";
                    })
                    $("#tmpImg").html(html)
                } else {
                    alert("保存失败")
                }
            },
        })
    })

    //配置模态框点击确认
    $("#ok").click(function () {
        var test = paint.getCoordinate();
        var title = $("#exampleModalLabel").html();
        if (title === "设置检测区域") {
            $("#setStartPoint").val(Math.round(test[0].minX) + "," + Math.round(test[0].minY))
            // $("#setEndPoint").val(Math.round(test[0].maxX) + "," + Math.round(test[0].maxY))
        } else if (title === "设置边界线") {
            $("#setBorderline").val(Math.round(test[0].minX) + "," + Math.round(test[0].minY) + " " + Math.round(test[0].maxX) + "," + Math.round(test[0].maxY))
        }

        $("#exampleModal").modal('hide');
    })


    // 设置界面请求图片进行画图
    $("#setArea").click(function () {
        $("#exampleModalLabel").html("设置检测区域");
        if (selectDevice === '') {
            alert("未选择设备");
            return;
        }
        var json = {"deviceId": selectDevice};
        $.ajax({
            url: '/getBackground',
            type: 'post',
            data: json,
            //FIXME 需要添加当前请求的设备id
            dataType: 'json',
            success: function (data) {
                $("#canvas").attr("width", data.width);
                $("#canvas").attr("height", data.height);
                $("#drawModal").attr("style", "width:" + (data.width * 1 + 30) + "px");
                paint.init();
                paint.setBackground(data.imgUrl);
                paint.setType(false);
                $("#exampleModal").modal('show');
                //新增
                var c = document.getElementById("canvas");
                var ctx = c.getContext("2d");
                var img = new Image();
                img.src = data.imgUrl;

                img.onload = function () {
                    ctx.drawImage(img, 0, 0);
                }
            }
        })

    })


    $("#setLine").click(function () {
        $("#exampleModalLabel").html("设置边界线");
        if (selectDevice === '') {
            alert("未选择设备");
            return;
        }
        var json = {"deviceId": selectDevice};
        $.ajax({
            url: '/getBackground',
            type: 'post',
            data: json,
            dataType: 'json',
            success: function (data) {
                $("#canvas").attr("width", data.width);
                $("#canvas").attr("height", data.height);
                $("#drawModal").attr("style", "width:" + (data.width + 30) + "px");
                paint.init();
                paint.setBackground(data.imgUrl);
                paint.setType(true);
                var c = document.getElementById("canvas");
                var ctx = c.getContext("2d");
                var img = new Image();
                img.src = data.imgUrl;
                img.onload = function () {
                    ctx.drawImage(img, 0, 0);
                }
            }
        })
    })


    // 生成统计图表
    var deviceChart = function (data_x, data_normal, data_extreme) {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('main'));

        // 指定图表的配置项和数据
        var option = {
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data: ['严重预警', '普通预警'],
                left: 'right'
            },
            xAxis: {
                type: 'category',
                boundaryGap: false,
                data: data_x
            },
            yAxis: {
                type: 'value',
                name: '次',
                axisLabel: {
                    formatter: '{value}'
                }
            },
            dataZoom: [
                {
                    show: true,
                    realtime: true,
                    start: 0,
                    end: 100
                },
                {
                    type: 'inside',
                    realtime: true,
                    start: 65,
                    end: 85
                }
            ],
            series: [
                {
                    name: '严重预警',
                    type: 'line',
                    data: data_extreme
                },
                {
                    name: '普通预警',
                    type: 'line',
                    data: data_normal
                }
            ]
        };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
    }


    //添加统计图表的数据
    var getCharts = function (deviceId) {
        var json = {"deviceId": deviceId};
        $.ajax({
            url: '/chart',
            type: 'post',
            data: json,
            dataType: 'json',
            success: function (data) {
                //添加折线图的值
                deviceChart(data.data_x, data.data_normal, data.data_extreme);
            }
        })
    }
    getCharts("all")


    // 历史记录中生成分页和表格
    $("#tablePage").click(function (e) {
        var pageId = $(e.target).parents("li")[0].id;
        var deviceId = $("#selectDevice").val().replace("select", "")
        deviceId = deviceId === "all" ? "" : deviceId;
        changePage(pageId, "tablePage", "/viewHistory", deviceId);
    })


    //点击预警信息时触发（默认全部设备）
    $("#lookHistory").click(function () {
        var json = {'deviceId': '', 'page': ''};
        $.ajax({
            url: '/viewHistory',
            type: 'post',
            data: json,
            dataType: 'json',
            success: function (data) {
                $("#tablePageMaxPage").val(data.maxPage);
                var html = "";
                $.each(data.list, function (n, value) {
                    html += "<tr>";
                    $.each(value, function (i, item) {
                        if (i == 3) {
                            html += "<td class=\"HistoryDetail\">详情<input type=\"text\" style=\"display: none;\" value=\"" + item + "\"></td>"
                        } else
                            html += "<td>" + item + "</td>"
                    })
                    html += "</tr>"
                })
                $("#historyBody").html(html);
                initPage(data.maxPage, "tablePage");
            }
        })
    })


    //在预警信息中选择查看哪个设备的历史记录
    $("#downMenu1").click(function (e) {
        var device = $(e.target).parents("li")[0].id;
        var json = '';
        $("#selectDevice").val(device);
        var select = $("#" + device).children("a").html()
        $("#dropdownMenu1").html(select + " <span class=\"caret\"></span>");
    })
    $("#downMenu2").click(function (e) {
        var device = $(e.target).parents("li")[0].id;
        var json = '';
        $("#selectDevice").val(device);
        var select = $("#" + device).children("a").html()
        $("#dropdownMenu2").html(select + " <span class=\"caret\"></span>");
    })
        //新增
    $("#query").click(function(){
        var selectDevice = $("#dropdownMenu1").html().replace("<span class=\"caret\"></span>","").trim()
        var selectLevel = $("#dropdownMenu2").html().replace("<span class=\"caret\"></span>","").trim()
        var startTime = $("#datepicker1").val()
        var endTimme = $("#datepicker2").val()
        var json = {'page': '', "deviceId": selectDevice, "waringType": selectLevel,"startTime":startTime,"endTimme":endTimme}
        $.ajax({
            url: '/viewHistory',
            type: 'post',
            data: json,
            dataType: 'json',
            success: function (data) {
                $("#maxPage").val(data.maxPage);
                var html = "";
                $.each(data.list, function (n, value) {
                    html += "<tr>";
                    $.each(value, function (i, item) {
                        if (i == 3) {
                            html += "<td class=\"HistoryDetail\">详情<input type=\"text\" style=\"display: none;\" value=\"" + item + "\"></td>"
                        } else
                            html += "<td>" + item + "</td>"
                    })
                    html += "</tr>"
                })
                $("#historyBody").html(html);
                initPage(data.maxPage, "tablePage")
            }
        })
    })


    //分页函数
    var dividePage = function (prefix, page, index, isLeft) {
        var tmpPage = "";
        var tmp = $("#" + prefix).html();
        if (page.length <= 8) {
            tmpPage += "<li class=\"pagination\" id=\"" + prefix + "LeftPage\"><a><span aria-hidden=\"true\" >&laquo;</span></a></li>";
            for (var i = 1; i <= page.length; i++) {
                if (i == index * 1) {
                    tmpPage += "<li class=\"active\" id=\"" + prefix + (i * 1) + "\"><a>" + (i * 1) + "</a></li>"
                } else {
                    tmpPage += "<li class=\"pagination\" id=\"" + prefix + (i * 1) + "\"><a>" + (i * 1) + "</a></li>"
                }
            }
            tmpPage += "<li class=\"pagination\" id=\"" + prefix + "RightPage\"><a><span aria-hidden=\"true\">&raquo;</span></a></li>";

        } else if (page.length - index < 8) {
            tmpPage += "<li class=\"pagination\" id=\"" + prefix + "LeftPage\"><a><span aria-hidden=\"true\" >&laquo;</span></a></li>";
            for (var i = page.length - 7; i <= page.length; i++) {
                if (i == index * 1) {
                    tmpPage += "<li class=\"active\" id=\"" + prefix + (i * 1) + "\"><a>" + (i * 1) + "</a></li>"
                } else {
                    tmpPage += "<li class=\"pagination\" id=\"" + prefix + (i * 1) + "\"><a>" + (i * 1) + "</a></li>"
                }
            }
            tmpPage += "<li class=\"pagination\" id=\"" + prefix + "RightPage\"><a><span aria-hidden=\"true\">&raquo;</span></a></li>";

        } else if (index <= 4) {
            tmpPage += "<li class=\"pagination\" id=\"" + prefix + "LeftPage\"><a><span aria-hidden=\"true\" >&laquo;</span></a></li>";
            for (var i = 1; i < ((page.length - index + 1) < 6 ? (page.length - index + 1) : 6); i++) {
                if (i == index * 1) {
                    tmpPage += "<li class=\"active\" id=\"" + prefix + (i * 1) + "\"><a>" + (i * 1) + "</a></li>"
                } else {
                    tmpPage += "<li class=\"pagination\" id=\"" + prefix + (i * 1) + "\"><a>" + (i * 1) + "</a></li>"
                }
            }
            if (page.length - index * 1 + 1 > 6) {
                tmpPage += "<li class=\"pagination\" id=\"" + prefix + "0\"><a>...</a></li>" +
                    "<li class=\"pagination\" id=\"" + prefix + page.length + "\"><a>" + page.length + "</a></li>";
            }
            tmpPage += "<li class=\"pagination\" id=\"" + prefix + "RightPage\"><a><span aria-hidden=\"true\">&raquo;</span></a></li>";

        } else {
            tmpPage += "<li class=\"pagination\" id=\"" + prefix + "LeftPage\"><a><span aria-hidden=\"true\" >&laquo;</span></a></li>";
            for (var i = (index - 4); i <= (index * 1 + 1); i++) {
                if (i == index * 1) {
                    tmpPage += "<li class=\"active\" id=\"" + prefix + (i * 1) + "\"><a>" + (i * 1) + "</a></li>"
                } else {
                    tmpPage += "<li class=\"pagination\" id=\"" + prefix + (i * 1) + "\"><a>" + (i * 1) + "</a></li>"
                }
            }
            tmpPage += "<li class=\"pagination\" id=\"" + prefix + "0\"><a>...</a></li>" +
                "<li class=\"pagination\" id=\"" + prefix + page.length + "\"><a>" + page.length + "</a></li>";
            tmpPage += "<li class=\"pagination\" id=\"" + prefix + "RightPage\"><a><span aria-hidden=\"true\">&raquo;</span></a></li>";
        }
        return tmpPage;
    }

    //点击分页
    var changePage = function (pageId, eid, url, data) {
        var activeId = $("#" + eid).children(".active")[0].id;
        var activeLen = activeId.length;
        var pageLen = pageId.length;
        var maxPage = eid.replace("Page", "");
        var idLen = eid.length;
        var isLeft = false;
        if (pageId.indexOf("LeftPage") != -1 && activeId.substring(idLen, activeLen) != "1") {
            pageId = activeId.slice(0, idLen) + (activeId.substring(idLen, activeLen) * 1 - 1);
            isLeft = true;
        } else if (pageId.indexOf("LeftPage") != -1 && activeId.substring(idLen, activeLen) === "1" || pageId === eid + "0") {
            return;
        } else if (pageId.indexOf("RightPage") != -1 && activeId.substring(idLen, activeLen) != $("#" + maxPage + "MaxPage").val()) {
            pageId = activeId.slice(0, idLen) + (activeId.substring(idLen, activeLen) * 1 + 1);

        } else if (pageId.indexOf("RightPage") != -1 && activeId.substring(idLen, activeLen) === $("#" + maxPage + "MaxPage").val()) {
            return;
        }
        if (eid === "imagePage") {
            var json = {"temp_page": pageId.substring(idLen, pageLen), "dataset_page": 1};
        } else if (eid === "asidePage") {
            var json = {"dataset_page": pageId.substring(idLen, pageLen), "temp_page": 1, "imgId": data};
        } else
            var json = {"page": pageId.substring(idLen, pageLen), "deviceId": data};

        $.ajax({
            url: url,
            type: 'post',
            data: json,
            dataType: 'json',
            success: function (data) {
                if (eid === "imagePage") {
                    setMidImage(data.temp);
                    var page = {"length": data.temp_maxpage}
                } else if (eid === "asidePage") {
                    setHistoryTable(data.dataset);
                    var page = {"length": data.dataset_maxpage}
                } else if (eid === "tablePage") {
                    setTable(data.list);
                    var page = {"length": data.maxPage}

                }
                var html = dividePage(eid, page, pageId.substring(idLen, pageId.length), isLeft);

                if (html != "") {
                    $("#" + eid).html(html);
                } else {
                    $("#" + activeId).attr("class", "pagination");
                    $("#" + pageId).attr("class", "active");
                    $("#" + maxPage + "MaxPage").val(page.length);
                }

            }
        })
    }


    //训练部分设置右边展示的照片  list=[{"imgeId": "dfnd","src":"url"}]
    var setHistoryTable = function (list) {
        var html = "";
        $.each(list, function (i, item) {
            if (i == 0) {
                html += "<div class=\"row col-lg-12 side-context\">" +
                    "<div id=\"image" + i + "\" class=\"col-md-4 col-sm-4 display-image aside-imgae\">" +
                    "<div class=\"grey-panel pn donut-chart\">" +
                    "<img src=\"" + item.src + "\" height=\"25%\" width=\"100%\" alt=\"" + item.id + "\"/>" +
                    "</div>" +
                    "</div>";
            } else if (i % 3 == 0) {
                html += "</div>" +
                    "<div class=\"row col-lg-12 side-context\">" +
                    "<div id=\"image" + i + "\" class=\"col-md-4 col-sm-4 display-image aside-imgae\">" +
                    "<div class=\"grey-panel pn donut-chart\">" +
                    "<img src=\"" + item.src + "\" height=\"25%\" width=\"100%\" alt=\"" + item.id + "\"/>" +
                    "</div>" +
                    "</div>";
            } else {
                html += "<div id=\"image" + i + "\" class=\"col-md-4 col-sm-4 display-image aside-imgae\">" +
                    "<div class=\"grey-panel pn donut-chart\">" +
                    "<img src=\"" + item.src + "\" height=\"25%\" width=\"100%\" alt=\"" + item.id + "\"/>" +
                    "</div>" +
                    "</div>";
            }
        })
        html += "</div>";
        $("#historyTable").html(html);
    }

    //训练部分中间所展示的照片
    var setMidImage = function (list) {
        var html = "";
        $.each(list, function (i, item) {
            if (i == 0) {
                html += "<div class=\"row mid-context\">" +
                    "<div id=\"img\" class=\"col-md-2 col-sm-2 display-image mindImage\">" +
                    "<div class=\"grey-panel pn donut-chart\">" +
                    "<img id=\"" + item.id + "\" src=\"" + item.src + "\" alt=\"" + item.width + "&" + item.height + "\" width=\"100%\"/>" +
                    "</div>" +
                    "</div>";
            } else if (i * 1 % 6 == 0) {
                html += "</div>" +
                    "<div class=\"row mid-context\">" +
                    "<div id=\"img\" class=\"col-md-2 col-sm-2 display-image mindImage\">" +
                    "<div class=\"grey-panel pn donut-chart\">" +
                    "<img id=\"" + item.id + "\" src=\"" + item.src + "\" alt=\"" + item.width + "&" + item.height + "\" width=\"100%\"/>" +
                    "</div>" +
                    "</div>";
            } else {
                html += "<div id=\"img\" class=\"col-md-2 col-sm-2 display-image mindImage\">" +
                    "<div class=\"grey-panel pn donut-chart\">" +
                    "<img id=\"" + item.id + "\" src=\"" + item.src + "\" alt=\"" + item.width + "&" + item.height + "\" width=\"100%\"/>" +
                    "</div>" +
                    "</div>";
            }
        })
        html += "<div>";
        $("#setMidImage").html(html)
    }

    //初始化分页
    var initPage = function (length, type) {
        var tmpPage = "";
        tmpPage += "<li class=\"pagination\" id=\"" + type + "LeftPage\"><a><span aria-hidden=\"true\" >&laquo;</span></a></li>";
        tmpPage += "<li class=\"active\" id=\"" + type + "1\"><a>1</a></li>"
        for (var i = 1; i < (length < 8 ? length : 8); i++) {
            tmpPage += "<li class=\"pagination\" id=\"" + type + (i * 1 + 1) + "\"><a>" + (i * 1 + 1) + "</a></li>"
        }
        if (length > 8) {
            tmpPage += "<li class=\"pagination\" id=\"" + type + "0\"><a>...</a></li>" +
                "<li class=\"pagination\" id=\"" + type + length + "\"><a>" + length + "</a></li>";
        }
        tmpPage += "<li class=\"pagination\" id=\"" + type + "RightPage\"><a><span aria-hidden=\"true\">&raquo;</span></a></li>";
        $("#" + type).html(tmpPage);
    }

    //训练中刚上传的图片的分页
    $("#imagePage").click(function (e) {
        var pageId = $(e.target).parents("li")[0].id;
        changePage(pageId, "imagePage", "/getPhotos", null);
    })

    //训练部分中间所展示照片的分页
    $("#asidePage").click(function (e) {
        var pageId = $(e.target).parents("li")[0].id;
        changePage(pageId, "asidePage", "/getPhotos", null);
    })


    var setTable = function (list) {
        var html = "";
        $.each(list, function (n, value) {
            html += "<tr>";
            $.each(value, function (i, item) {
                if (i == 3) {
                    html += "<td class=\"detail\">详情<input type=\"text\" style=\"display: none;\" value=\"" + item + "\"></td>"
                } else
                    html += "<td id='loc'" + n * 10 + i + ">" + item + "</td>"
            })
            html += "</tr>"
        })
        $("#historyBody").html(html);
    }

    //主页中获得右侧table中的值
    var getTable = function () {
        var json = "";
        if (currentDevice === "") {
            json = {"deviceId": "all"}
        } else {
            json = {"deviceId": currentDevice}
        }
        $.ajax({
            url: '/warningRecord',
            type: 'post',
            data: json,
            dataType: 'json',
            success: function (data) {
                var html = "";
                $.each(data, function (n, value) {
                    html += "<tr>";
                    $.each(value, function (i, item) {
                        if (i == 3) {
                            html += "<td class=\"detail\">详情<input type=\"text\" style=\"display: none;\" value=\"" + item + "\"></td>"
                        } else
                            html += "<td id='loc'" + n * 10 + i + ">" + item + "</td>"
                    })
                    html += "</tr>"
                })
                $("#tbody").html(html);
            }
        })
    }


    getTable()
    setInterval(getTable, 2000);


    var deleteRight = function (pageId, type, url, deviceId) {
        var json = {"imgId": deviceId}
        $.ajax({
            url: '/deleteDB',
            type: 'post',
            data: json,
            dataType: 'json',
            success: function (data) {
                if (data.boo == true) {
                    changePage(pageId, type, url, null)
                    $("#exampleModal4").modal('hide')
                }
            }
        })
    }

    //训练部分点击中间展示的图片，将图片加载到画布
    $(document).on("click", ".mindImage", function (e) {
        var obj = "";
        if (e.target.id === 'img') {
            obj = $(e.target).children().children();
        } else {
            obj = $(e.target);
        }
        var tmp = $("#ImgId").val();
        if (tmp != obj[0].id) {
            $("#tmpImg").html("");
            $("#ImgId").val(obj[0].id)
        }
        var tmp = obj[0].alt;
        var wh = tmp.split("&");
        $("#drawImage").attr("width", wh[0]);
        $("#drawImage").attr("height", wh[1]);
        $("#drawModal2").attr("style", "width:" + (wh[0] * 1 + 30) + "px");
        paint2.init();

        var parent = $("#" + obj[0].id).parent().parent();
        if ($(parent).attr("class").indexOf("select-img") == -1) {
            getTmpTable(obj[0].id)
            $(".mindImage").attr("class", "col-md-2 col-sm-2 display-image mindImage")
            $(parent).attr("class", "col-md-2 col-sm-2 display-image mindImage select-img");
            return;
        }
        $("#ImgId").val(obj[0].id)
        var c = document.getElementById("drawImage");
        var ctx = c.getContext("2d");
        var img = new Image();
        img.src = obj[0].src;
        paint2.setBackground(img.src)
        img.onload = function () {
            ctx.drawImage(img, 0, 0);
        }
        $("#dropdownMenu2").html("异物类型" + "<span class=\"caret\"></span>");
        $(".mindImage").attr("class", "col-md-2 col-sm-2 display-image mindImage");
        $(e.target).parents("#img").attr("class", "col-md-2 col-sm-2 display-image mindImage select-img")
        $("#exampleModal5").modal('show');
    })
    var lookDetailObject = ""
    $(document).on("click", ".detail", function (e) {
        lookDetailObject = "datail";
        $("#detailImg").attr("src", $(e.target).children("input").val());
        $("#exampleModal4").modal('show');
	$(".detail-bar").hide();
    })

    $(document).on("click", ".HistoryDetail", function (e) {
        lookDetailObject = "history";
        $("#detailImg").attr("src", $(e.target).children("input").val());
        // $("#exampleModal3").modal('hide');
        $("#exampleModal4").modal('show');
	$(".detail-bar").hide();
    })


    $("#datailClose").click(function () {
        if (lookDetailObject === "history") {
            $("#exampleModal3").modal('show');
        }
    })

    $(document).on("click", ".aside-imgae", function (e) {
        var parent = $(e.target).parents(".display-image");
        $(".aside-imgae").attr("class", "col-md-4 col-sm-4 display-image aside-imgae");
        parent.attr("class", "col-md-4 col-sm-4 display-image aside-imgae select-img");
        $(".side-context").attr("class", "row col-lg-12 side-context");
        parent.parent().attr("class", "row col-lg-12 side-context select-block");
        $(".detail-bar").show();
        $("#deleteImg").attr("class", "btn btn-default footer-btn historyDelete")
        $(".btn").show();
        lookImg();
    })
    var lookImg = function () {
        var imgUrl = $("#historyTable").children(".select-block").children(".select-img").children().children()[0].src;
        $("#detailImg").attr("src", imgUrl);
        $("#exampleModal4").modal("show");

    }

    $("#deleteImg").click(function () {
        var type = $("#deleteImg").attr("class");
        if (type.indexOf("tmpDelete") != -1) {
            tmpDelete();
        } else if (type.indexOf("historyDelete") != -1) {
            var imgId = $("#historyTable").children(".select-block").children(".select-img").children().children()[0].alt;
            var pageId = $("#asidePage").children(".active")[0].id;
            deleteRight(pageId, "asidePage", "/getPhotos", imgId);
        }
    })

    var getTmpTable = function (imgId) {
        var json = {"imgId": imgId}
        $.ajax({
            url: '/viewSteps',
            type: 'post',
            data: json,
            dataType: 'json',
            success: function (data) {
                if (data.boo == true) {
                    var html = "";
                    $.each(data.list, function (n, value) {
                        html += "<div id=\"img\" class=\"col-md-2 col-sm-2 display-image tmpImg\">" +
                            "<div class=\"grey-panel pn donut-chart\">" +
                            "<img id=\"serverstatus1\" src=\"" + value.src + "\" width=\"100%\" alt=\"" + value.id + "\"/>" +
                            "</div>" +
                            "</div>";

                    })
                    $("#tmpImg").html(html)
                }
            }
        })
    }

    var resetRight = function (pageId1, pageId2, type1, type2, url, deviceId) {
        var json = {"imgId": deviceId}
        $.ajax({
            url: '/redrawDB',
            type: 'post',
            data: json,
            dataType: 'json',
            success: function (data) {
                if (data.boo == true) {
                    changePage(pageId1, type1, url, null)
                    changePage(pageId2, type2, url, null)
                    $("#exampleModal4").modal('hide')
                }
            }
        })
    }

    $("#resetImg").click(function () {
        var img_id = $("#historyTable").children(".select-block").children(".select-img").children().children()[0].alt;
        var pageId1 = $("#asidePage").children(".active")[0].id;
        var pageId2 = $("#imagePage").children(".active")[0].id;
        resetRight(pageId1, pageId2, "asidePage", "imagePage", "/getPhotos", img_id);
        //    FIXME redrawDB应该只负责更新数据库状态，不应该进行页面的更新
    })
    $(".type-dropwn").click(function (e) {
        var device = $(e.target).parents("li")[0].id;
        var select = $("#" + device).children("a").html();
        console.log($("#" + device).children())
        console.log(device)
        $(".selectDrop").attr("class", "selectDrop");
        $("#dropdownMenu2").html(select + "<span class=\"caret\"></span>");
        $("#" + device).attr("class", "_active selectDrop");
    })

    $("#lookImg").click(function () {
        var imgUrl = $("#historyTable").children(".select-block").children(".select-img").children().children()[0].src;
        $("#detailImg").attr("src", imgUrl);
        $("#exampleModal4").modal("show");
    })


    $(document).on("click", ".tmpImg", function (e) {
        var obj = "";
        if (e.target.id === 'img') {
            obj = $(e.target).children().children();
        } else {
            obj = $(e.target);
        }
        // $("#ImgId").val(obj[0].id)
        $(".tmpImg").attr("class", "col-md-2 col-sm-2 display-image tmpImg");
        $(e.target).parents("#img").attr("class", "col-md-2 col-sm-2 display-image tmpImg select-img")
        $(".tmp-btn").attr("disabled", false)
    })


    $("#tmpSave").click(function (e) {
        var imgId = $("#ImgId").val();
        var json = {"imgId": imgId}
        console.log(imgId + 'hnbghj')
        var html = $("#tmpImg").html();
        if (html === "") {
            return;
        }
        var pageId1 = $("#asidePage").children(".active")[0].id;
        var pageId2 = $("#imagePage").children(".active")[0].id;
        $.ajax({
            url: '/savePhoto',
            type: 'post',
            data: json,
            dataType: 'json',
            success: function (data) {
                if (data.boo == true) {
                    //FIXME 修改
                    // alert("保存成功");
                    var html = "保存成功"
                    $("#content").html(html)
                    $("#message").modal("show");
                    $("#tmpImg").html("");
                    changePage(pageId1, "asidePage", '/getPhotos', null)
                    changePage(pageId2, "imagePage", '/getPhotos', null)

                }
            }
        })
    })


    var lookTmp = function () {
        var imgUrl = $("#tmpImg").children(".select-img").children().children()[0].src;
        $("#detailImg").attr("src", imgUrl);
        $("#exampleModal4").modal('show');
    }

    $(document).on("click", ".tmpImg", function (e) {
        var obj = "";
        if (e.target.id === 'img') {
            obj = $(e.target).children().children();
        } else {
            obj = $(e.target);
        }
        // $("#ImgId").val(obj[0].alt)
        $(".tmpImg").attr("class", "col-md-2 col-sm-2 display-image tmpImg");
        $(e.target).parents("#img").attr("class", "col-md-2 col-sm-2 display-image tmpImg select-img")
        $(".detail-bar").show();
        $("#deleteImg").attr("class", "btn btn-default footer-btn tmpDelete")
        $("#resetImg").hide();
        lookTmp();
    })


    var tmpDelete = function (e) {
        var obj = $("#tmpImg").children(".select-img");
        var imgId = obj.children().children()[0].alt;
        var json = {"imgId": imgId}
        $.ajax({
            url: '/deleteStep',
            type: 'post',
            data: json,
            dataType: 'json',
            success: function (data) {
                if (data.boo == true) {
                    obj.remove();
                    $("#exampleModal4").modal('hide')
                }
            }
        })
    }
    $("#startExercise").click(function () {
        $("#SmallModal").modal("show");
    });
    $("#isExercise").click(function () {
        $.ajax({
            url: '/training',
            type: 'post',
            data: '',
            dataType: 'json',
            success: function (data) {
                if (data.boo == true) {
                    alert("训练完成")
                }
            }
        })
    })


    $(".block").dblclick(function(e){
        console.log($(e.target))
        var tabId = $(e.target).context.id
        var ttt = tabId.indexOf("device") > -1 ? "serverstatus" + tabId.replace("device",""):tabId;
        $("#fullScr-id").val(ttt);
        
        $("#fullScreen").modal("show");
        var width = document.body.clientWidth;
        var height = window.screen.height - 3;
        $("#drawModal3").attr("style", "width:" + width + "px;");
        $("#single").attr("style", "height:" + height + "px;width:" + (height * 16 / 9) + "px;padding-left:" + ((width - height * 16 / 9)) + "px;");
        // $("#single").attr("src", "/camera_feed/" + cameraId + "/1");
        fullScreen()
        closeFullScreen()
    })


    $("#closeFullScr").click(function () {
        exitScreen();
        openFullScreen()
    });

    var isFull = 0
    //全屏
    function fullScreen() {
        var el = document.documentElement;
        var rfs = el.requestFullScreen || el.webkitRequestFullScreen || el.mozRequestFullScreen || el.msRequestFullscreen;
        if (typeof rfs != "undefined" && rfs) {
            rfs.call(el);
        }
        ;
        return;
    }

    //退出全屏
    function exitScreen() {
        $("#single").attr("src", "");
        if (document.exitFullscreen) {
            document.exitFullscreen();
        } else if (document.mozCancelFullScreen) {
            document.mozCancelFullScreen();
        } else if (document.webkitCancelFullScreen) {
            document.webkitCancelFullScreen();
        } else if (document.msExitFullscreen) {
            document.msExitFullscreen();
        }
        if (typeof cfs != "undefined" && cfs) {
            cfs.call(el);
        }
    }

    // function closeFullScreen() {
    //     $(".midImage").attr("src", "")
    // }

    // function openFullScreen() {
    //     for (var i = 1; i <= 4; i++) {
    //         $("#serverstatus" + i).attr("src", "/camera_feed/" + i + "/0")
    //     }
    // }

    $("#single").dblclick(function () {
        openFullScreen();
        $("#fullScreen").modal("hide");
        exitScreen();
    })

    $(document).keyup(function (e) {
        var key = e.which || e.keyCode;
        if (key == 27) {
            openFullScreen();
            $("#fullScreen").modal("hide");
            exitScreen();
        }
    });
    var isFull = false
    window.onresize = function () {
        var ch = document.body.clientHeight;
        var sh = document.body.scrollHeight;
        if (isFullscreen && isFull == true) {
            //要执行的动作
            console.log(111 + isFull)
            isFull = false;
            openFullScreen();
            $("#fullScreen").modal("hide");
            exitScreen();
        } else if (isFullscreen && isFull == false) {
            isFull = true;
        }

    }

    function isFullscreen() {
        return document.fullscreenElement ||
            document.msFullscreenElement ||
            document.mozFullScreenElement ||
            document.webkitFullscreenElement || false;
    }

    var dateformat = { 
        /* 区域化周名为中文 */
        dayNamesMin : ["日", "一", "二", "三", "四", "五", "六"],  
        /* 每周从周一开始 */
        firstDay : 1,
        /* 区域化月名为中文习惯 */
        monthNames : ["01", "02", "03", "04", "05", "06",
                    "07", "08", "09", "10", "11", "12"],
        /* 月份显示在年后面 */
        showMonthAfterYear : true,
        /* 年份后缀字符 */
        yearSuffix : "年",
        monthSuffix : "月",
        /* 格式化中文日期
        （因为月份中已经包含“月”字，所以这里省略） */
        dateFormat : "yy-MM-dd"  
    }
    $( "#datepicker1").datepicker(dateformat);
    $( "#datepicker2").datepicker(dateformat);
    
    var videoPlay = function(video,videoUrl){
        if (Hls.isSupported()) {
            var hls = new Hls();
            hls.loadSource(videoUrl);
            hls.attachMedia(video);
            hls.on(Hls.Events.MANIFEST_PARSED, function () {
            video.play();
            });
        }else if (video.canPlayType('application/vnd.apple.mpegurl')) {
            video.src = videoUrl;
            video.addEventListener('loadedmetadata', function () {
            video.play();
            });
        }
    }
    
    var initVideo = function() {
        for (var i = 1; i <= 10; i++) {
            var video = document.getElementById("serverstatus" + i);
            videoPlay(video,"http://192.168.20.25:8080/hls/device" + i + ".m3u8")
        }
    }
    initVideo();
})


