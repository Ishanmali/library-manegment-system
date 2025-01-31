

<script>
// custamize qr code//
var qrcode = new QRCode("diplay", {
    text: "http://jindo.dev.naver.com/collie",
    width: 128,
    height: 128,
    colorDark : "#000000",
    colorLight : "red",
    correctLevel : QRCode.CorrectLevel.H
});
const inp= document.getElementById("in");
inp.addEventListener("keyup",function(){
    const view= inp.value;
    qrcode.makeCode(view); 
})
const down =document.getElementById("download");
down.addEventListener("click", function(){
    const img= document.getElementById("display  img");
    let link =document.createElement("a");
    link.href= img.src;
    link.download="qrcode.png";
    link.click()

})

</script>

