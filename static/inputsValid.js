var today = new Date();
var maxDate = new Date(today.getFullYear(), today.getMonth(), today.getDate());
document.getElementById('date').setAttribute('max', maxDate.toISOString().split('T')[0]);

function validateForm() {
    // Check if the inputs are equal
    var input1Value = document.getElementById("input1").value;
    var input2Value = document.getElementById("input2").value;

    if (input1Value !== input2Value) {
        alert("Inputs are not equal. Please correct and try again.");
        return false; // Prevent form submission
    }

    // Add additional validation or processing if needed

    return true; // Allow form submission
}