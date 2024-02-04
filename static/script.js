$(document).ready(function() {
    $('#zipTable').DataTable({
        paging: true,
        lengthMenu: [15, 30, 50, 100],
        searching: true,
        ordering: false
    });
});

function searchZipCode() {
    const searchInput = document.getElementById('searchTerm');
    const dataTable = $('#zipTable').DataTable();

    dataTable.search(searchInput.value).draw();
}