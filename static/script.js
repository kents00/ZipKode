$(document).ready(function () {
    // Initialize DataTable with enhanced features
    $('#zipTable').DataTable({
        responsive: true,
        pageLength: 10,
        dom: '<"row"<"col-sm-12 col-md-6"l><"col-sm-12 col-md-6"f>>' +
            '<"row"<"col-sm-12"tr>>' +
            '<"row"<"col-sm-12 col-md-5"i><"col-sm-12 col-md-7"p>>',
        language: {
            search: "Search records:",
            lengthMenu: "Show _MENU_ entries",
        }
    });

    // Add hover effects to table rows
    $('#zipTable tbody').on('mouseenter', 'tr', function () {
        $(this).addClass('highlight-row');
    }).on('mouseleave', 'tr', function () {
        $(this).removeClass('highlight-row');
    });

    // Smooth scroll to top
    $('.btn').addClass('animate__animated animate__pulse');

    // Add loading animation
    $(window).on('load', function () {
        $('.container').fadeIn('slow');
    });

    // Add tooltip to the donate button
    $('[data-toggle="tooltip"]').tooltip();
});

function searchZipCode() {
    const searchInput = document.getElementById('searchTerm');
    const dataTable = $('#zipTable').DataTable();

    dataTable.search(searchInput.value).draw();
}
