$(document).ready(function(){
    var paint = { 
	    init: function() { 
	        this.load(); 
	    }, 
        load: function() { 
	        this.x=[];//记录鼠标移动是的X坐标 
	        this.y=[];//记录鼠标移动是的Y坐标 
	        this.maxX=0;
	        this.maxY=0;
	        this.minX=123123123;
	        this.minY=123123123;
	        this.coordinate=[];
	        this.clickDrag=[]; 
	        this.img = new Image;
	        this.lock=false;//鼠标移动前，推断鼠标是否按下 
	        this.isEraser=false; 
	        this.storageColor="#FF0000";
	        this.fontWeight=[2,5,8]; 
	        this.$ = function(id){
	          return typeof id=="string"? document.getElementById(id):id;
	        }, 
	        this.canvas=this.$("canvas"); 
	        if (!this.canvas.getContext) { 
	          alert("您的浏览器不支持 canvas 标签"); 
	          return; 
	        } 
	        this.cxt=this.canvas.getContext('2d'); 
	        this.cxt.lineJoin = "round";//context.lineJoin - 指定两条线段的连接方式 
	        this.cxt.lineWidth = 1;//线条的宽度 
	        this.cxt.strokeStyle = "#FF0000"; 
	        this.iptClear=this.$("clear"); 
	        this.revocation=this.$("revocation");
	        this.w=this.canvas.width;//取画布的宽 
      		this.h=this.canvas.height;//取画布的高  
	        this.touch =("createTouch" in document);//判定是否为手持设备 
	        this.StartEvent = this.touch ? "touchstart" : "mousedown";//支持触摸式使用相应的事件替代 
	        this.MoveEvent = this.touch ? "touchmove" : "mousemove"; 
	        this.EndEvent = this.touch ? "touchend" : "mouseup";  
	        this.bind();
        }, 
    	bind: function() { 
      		var t=this; 
      		/*清除画布*/ 
	        this.iptClear.onclick = function() { 
	          t.clear();
			  var img = new Image();
			  img.src = "C:/Application/sublime/project/detectSystem/img/1.jpg";
			  img.onload = function()
			  {
			     t.cxt.drawImage(img,0,0);
			  } 
	        }; 
           /*鼠标按下事件，记录鼠标位置。并绘制，解锁lock，打开mousemove事件*/ 
	      this.canvas['on'+t.StartEvent]  =  function(e) {
//	      	  console.log($("#canvas").offset().left+" "+$("#canvas").offset().top) 
	          var touch=t.touch ? e.touches[0] : e; 
	          var _x=touch.pageX - $("#canvas").offset().left  //touch.target.offsetLeft;//鼠标在画布上的x坐标，以画布左上角为起点 
	          var _y=touch.pageY - $("#canvas").offset().top   //touch.target.offsetTop;//鼠标在画布上的y坐标，以画布左上角为起点 
//	          console.log(touch.pageY+" hahaha "+$("#canvas").offset().top);
	          if(t.isEraser) {
//	          	console.log(this.minX+" "+this.minY+" "+this.maxX+" "+this.maxY) 
	            t.resetEraser(_x,_y,touch); 
	          }else { 
	            t.movePoint(_x,_y);//记录鼠标位置 
	            t.drawPoint();//绘制路线 
	          } 
	            t.lock=true; 
	        }; 
           /*鼠标移动事件*/ 
    	   this.canvas['on'+t.MoveEvent] = function(e) { 
		       e.stopPropagation();////////////////////////////////////////////////禁止冒泡事件/////////////////////////////////////////
		       var touch=t.touch ? e.touches[0] : e; 
		       //t.lock为true则运行
		       if(t.lock) { 
		          var _x=touch.pageX - $("#canvas").offset().left //touch.target.offsetLeft;//鼠标在画布上的x坐标，以画布左上角为起点 
		          var _y=touch.pageY - $("#canvas").offset().top //touch.target.offsetTop;//鼠标在画布上的y坐标。以画布左上角为起点 
//		         	console.log(_x+" bbbbbb "+_y);
		          if(t.isEraser) {
		          	// console.log(this.minX+" "+this.minY+" "+this.maxX+" "+this.maxY)
		          	// t.rect(this.minX,this.minY,this.maxX,this.maxY);
		           //  t.stroke(); 
		            t.resetEraser(_x,_y,touch);  
		          } else { 
		            t.movePoint(_x,_y,true);//记录鼠标位置 
		            t.drawPoint();//绘制路线 
		          } 
		        } 
            };
    		this.canvas['on'+t.EndEvent] = function(e) { 
		        /*重置数据*/ 
		        
		        // t.cxt.rect(t.minX,t.minY,t.maxX-t.minX,t.maxY-t.minY);
		        // t.cxt.stroke(); 
		        console.log(t.maxX+" max "+t.maxY)
		        var position = {"minX":t.minX,"minY":t.minY,"maxX":t.maxX,"maxY":t.maxY};
		        t.coordinate.push(position);
		        t.lock=false; 
		        t.x=[]; 
		        t.y=[];
		        t.maxX=0;
	        	t.maxY=0;
	       		t.minX=123123123;
	        	t.minY=123123123; 
		        t.clickDrag=[]; 
		        clearInterval(t.Timer); 
		        t.Timer=null; 
    		}; 
  		},
        //blind end 
	  	movePoint:function(x,y,dragging) { 
	      	/*将鼠标坐标加入到各自相应的数组里*/ 
	      	this.x.push(x); 
	      	this.y.push(y);
	      	this.maxX = this.maxX<x?x:this.maxX;
	      	this.maxY = this.maxY<y?y:this.maxY;
	      	this.minX = this.minX<x?this.minX:x;
	      	this.minY = this.minY<y?this.minY:y;
//	      	console.log(this.minX+" "+this.minY+" "+this.maxX+" "+this.maxY)
	      	this.clickDrag.push(y); 
	  	}, 
	    drawPoint:function(x,y,radius) { 
	      //循环数组
	      for(var i=0; i < this.x.length; i++) { 
	        this.cxt.beginPath();//context.beginPath() , 准备绘制一条路径 
	        if(this.clickDrag[i] && i){//当是拖动并且i!=0时，从上一个点開始画线。 
	          this.cxt.moveTo(this.x[i-1], this.y[i-1]);//context.moveTo(x, y) , 新开一个路径，并指定路径的起点 
	        }else{ 
	          this.cxt.moveTo(this.x[i]-1, this.y[i]); 
	        } 
	        this.cxt.lineTo(this.x[i], this.y[i]);//context.lineTo(x, y) , 将当前点与指定的点用一条笔直的路径连接起来 
	        this.cxt.closePath();//context.closePath() , 假设当前路径是打开的则关闭它 
	        this.cxt.stroke();//context.stroke() , 绘制当前路径
	        // this.cxt.rect(this.x[0],this.y[0],this.x[i]-this.x[0],this.y[i]-this.y[0]); 
	        // this.cxt.stroke();
	      } 
	    }, 
		clear:function() { 
		  this.cxt.clearRect(0, 0, this.w, this.h);//清除画布，左上角为起点 
		}, 
		getCoordinate: function() {
			return this.coordinate;
		},
		drawRect: function() {
			for(var i=0; i < this.coordinate.length; i++) {
				this.cxt.rect(this.coordinate[i].minX,this.coordinate[i].minY,this.coordinate[i].maxX-this.coordinate[i].minX,this.coordinate[i].maxY-this.coordinate[i].minY); 
	        	this.cxt.stroke();
			}
		},
		setBackground: function(imgUrl) {
			this.clear();
			this.img.src = imgUrl;
			img.onload = function()
			{
			     this.cxt.drawImage(img,0,0);
			} 
		}
 	};

(function(){ 
//     var paint = { 
// 	    init: function() { 
// 	        this.load(); 
// 	    }, 
//         load: function() { 
// 	        this.x=[];//记录鼠标移动是的X坐标 
// 	        this.y=[];//记录鼠标移动是的Y坐标 
// 	        this.clickDrag=[]; 
// 	        this.lock=false;//鼠标移动前，推断鼠标是否按下 
// 	        this.isEraser=false; 
// 	        this.storageColor="#FF0000";
// 	        this.fontWeight=[2,5,8]; 
// 	        this.$ = function(id){
// 	          return typeof id=="string"? document.getElementById(id):id;
// 	        }, 
// 	        this.canvas=this.$("canvas"); 
// 	        if (!this.canvas.getContext) { 
// 	          alert("您的浏览器不支持 canvas 标签"); 
// 	          return; 
// 	        } 
// 	        this.cxt=this.canvas.getContext('2d'); 
// 	        this.cxt.lineJoin = "round";//context.lineJoin - 指定两条线段的连接方式 
// 	        this.cxt.lineWidth = 1;//线条的宽度 
// 	        this.cxt.strokeStyle = "#FF0000"; 
// 	        this.iptClear=this.$("clear"); 
// 	        this.revocation=this.$("revocation");
// 	        this.w=this.canvas.width;//取画布的宽 
//       		this.h=this.canvas.height;//取画布的高  
// 	        this.touch =("createTouch" in document);//判定是否为手持设备 
// 	        this.StartEvent = this.touch ? "touchstart" : "mousedown";//支持触摸式使用相应的事件替代 
// 	        this.MoveEvent = this.touch ? "touchmove" : "mousemove"; 
// 	        this.EndEvent = this.touch ? "touchend" : "mouseup";  
// 	        this.bind();
//         }, 
//     	bind: function() { 
//       		var t=this; 
//       		/*清除画布*/ 
// 	        this.iptClear.onclick = function() { 
// 	          t.clear();
// 			  var img = new Image();
// 			  img.src = "C:/Application/sublime/project/detectSystem/img/1.jpg";
// 			  img.onload = function()
// 			  {
// 			     t.cxt.drawImage(img,0,0);
// 			  } 
// 	        }; 
//            /*鼠标按下事件，记录鼠标位置。并绘制，解锁lock，打开mousemove事件*/ 
// 	      this.canvas['on'+t.StartEvent]  =  function(e) {
// 	      	  console.log($("#canvas").offset().left+" "+$("#canvas").offset().top) 
// 	          var touch=t.touch ? e.touches[0] : e; 
// 	          var _x=touch.clientX - $("#canvas").offset().left  //touch.target.offsetLeft;//鼠标在画布上的x坐标，以画布左上角为起点 
// 	          var _y=touch.clientY - $("#canvas").offset().top   //touch.target.offsetTop;//鼠标在画布上的y坐标，以画布左上角为起点 
// 	          if(t.isEraser) { 
// 	            t.resetEraser(_x,_y,touch); 
// 	          }else { 
// 	            t.movePoint(_x,_y);//记录鼠标位置 
// 	            t.drawPoint();//绘制路线 
// 	          } 
// 	            t.lock=true; 
// 	        }; 
//            /*鼠标移动事件*/ 
//     	   this.canvas['on'+t.MoveEvent] = function(e) { 
// 		       e.stopPropagation();////////////////////////////////////////////////禁止冒泡事件/////////////////////////////////////////
// 		       var touch=t.touch ? e.touches[0] : e; 
// 		       //t.lock为true则运行
// 		       if(t.lock) { 
// 		          var _x=touch.clientX - $("#canvas").offset().left //touch.target.offsetLeft;//鼠标在画布上的x坐标，以画布左上角为起点 
// 		          var _y=touch.clientY - $("#canvas").offset().top //touch.target.offsetTop;//鼠标在画布上的y坐标。以画布左上角为起点 
// 		          if(t.isEraser) { 
// 		            t.resetEraser(_x,_y,touch);  
// 		          } else { 
// 		            t.movePoint(_x,_y,true);//记录鼠标位置 
// 		            t.drawPoint();//绘制路线 
// 		          } 
// 		        } 
//             };
//     		this.canvas['on'+t.EndEvent] = function(e) { 
// 		        /*重置数据*/ 
// 		        t.lock=false; 
// 		        t.x=[]; 
// 		        t.y=[]; 
// 		        t.clickDrag=[]; 
// 		        clearInterval(t.Timer); 
// 		        t.Timer=null; 
//     		}; 
// 		    // this.revocation.onclick = function() { 
// 		    //     t.redraw(); 
// 		    // }; 
//     		// /*橡皮擦*/ 
// 		    // this.$("eraser").onclick = function(e) { 
// 		    //     t.isEraser=true; 
// 		    //     t.$("error").style.color="red"; 
// 		    //     t.$("error").innerHTML="您已使用橡皮擦！"; 
// 		    // }; 
//   		},
//         //blind end 
// 	  	movePoint:function(x,y,dragging) { 
// 	      	/*将鼠标坐标加入到各自相应的数组里*/ 
// 	      	this.x.push(x); 
// 	      	this.y.push(y); 
// 	      	this.clickDrag.push(y); 
// 	  	}, 
// 	    drawPoint:function(x,y,radius) { 
// 	      //循环数组
// 	      for(var i=0; i < this.x.length; i++) { 
// 	        this.cxt.beginPath();//context.beginPath() , 准备绘制一条路径 
// 	        if(this.clickDrag[i] && i){//当是拖动并且i!=0时，从上一个点開始画线。 
// 	          this.cxt.moveTo(this.x[i-1], this.y[i-1]);//context.moveTo(x, y) , 新开一个路径，并指定路径的起点 
// 	        }else{ 
// 	          this.cxt.moveTo(this.x[i]-1, this.y[i]); 
// 	        } 
// 	        this.cxt.lineTo(this.x[i], this.y[i]);//context.lineTo(x, y) , 将当前点与指定的点用一条笔直的路径连接起来 
// 	        this.cxt.closePath();//context.closePath() , 假设当前路径是打开的则关闭它 
// 	        this.cxt.stroke();//context.stroke() , 绘制当前路径
// //	        this.cxt.rect(this.x[0],this.y[0],this.x[i]-this.x[0],this.y[i]-this.y[0]); 
// 	        this.cxt.stroke();
// 	      } 
// 	    }, 
// 		clear:function() { 
// 		  this.cxt.clearRect(0, 0, this.w, this.h);//清除画布，左上角为起点 
// 		}, 
//  	};
  paint.init(); 
})(); 
$("#ok").click(function() {
	var test=paint.getCoordinate();
	paint.drawRect();
	var c=document.getElementById("canvas");
	var ctx=c.getContext("2d");
	console.log(test.length);
	for(var i=0; i < test.length; i++) {
		// ctx.rect(test.minX,test.minY,test[i].manX-test[i].minX,test[i].manY-test[i].minY); 
	 //    ctx.stroke();
		console.log(test[i].minX+" "+test[i].minY+" "+test[i].maxX+" "+test[i].maxY)
	}
})

var c=document.getElementById("canvas");
var ctx=c.getContext("2d");
var img = new Image();
img.src = "C:/Application/sublime/project/detectSystem/img/1.jpg";
img.onload = function()
{
    ctx.drawImage(img,0,0);
}




})