function updateInputType() {
    var dropdown = document.getElementById("dropdown");
    var selectedColumn = dropdown.options[dropdown.selectedIndex].value;
    var inputField = document.getElementById("email");

    if (selectedColumn === "issue_date") {
        inputField.type = "date";
    } else {
        inputField.type = "text";
    }
}