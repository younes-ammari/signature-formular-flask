function printPage() {
    var printContent = document.getElementById("print_view");
    var originalContents = document.body.innerHTML;

    document.body.innerHTML = printContent.innerHTML;
    window.print();

    document.body.innerHTML = originalContents;
    console.log('clicked')
}
async function downloadPage() {
    var url = window.location.href; 
     // if you have static url you can hard code like
     // var url = "http://www.url.com";
    
     location.href = '/save'
    
    // fetch("/save")
}