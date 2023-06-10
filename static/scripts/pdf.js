function printPage() {
    var printContent = document.getElementById("print_view");
    var originalContents = document.body.innerHTML;

    document.body.innerHTML = printContent.innerHTML;
    window.print();

    document.body.innerHTML = originalContents;
    console.log('clicked')
}