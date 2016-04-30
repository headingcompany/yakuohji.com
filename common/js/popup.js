var HELPWin=null;//サブウインドウ
var HELPHref1="";//読み込むページ
function HelpWinOpen(HELPHref1,WinNo,W,H){
HELPWin=window.open(HELPHref1,WinNo,'toolbar=0,location=0,directories=0,status=0,menubar=0,scrollbars=1,resizable=1,width='+W+',height='+H+'');
//N2.0バグ回避用リピート
if(navigator.appVersion.charAt(0)==2){
HELPWin=window.open(HELPHref1,WinNo,'toolbar=0,location=0,directories=0,status=0,menubar=0,scrollbars=1,resizable=1,width='+W+',height='+H+'');}
//サブウインドウが開いたとき前面へフォーカスする。NN3.0~
if(navigator.appVersion.charAt(0)>=3){HELPWin.focus()}
};
<!---->
