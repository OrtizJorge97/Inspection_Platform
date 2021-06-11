console.log("Hello!!");
$('#navigateToNewPurchaseOrder').on('click', function() { 
	console.log("Navigating to grugru");
	window.location = '/AddPurchaseOrder'; 

});

$('#navigateToImportPurchaseOrder').on('click', function() { 
	console.log("Navigating to grugru");
	window.location = '/ImportPurchaseOrder'; 

});