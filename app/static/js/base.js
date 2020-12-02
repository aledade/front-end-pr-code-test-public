$(function() {
    const $loader = $('#loader');

    $("#addPetForm").submit((event) => {
        event.preventDefault();
        $loader.show();
        const userId = $(event.currentTarget).data('user-id');
        const formData = {};
        $(this).find("input").each((index, node) => {
            formData[$(node).attr('name')] = node.value;
        });
        $(this).find("select").each((index, node) => {
            formData[$(node).attr('name')] = $(node).find('option:selected').val();
        });
        $.ajax({
            url: `/api/users/${userId}/add_pet`,
            contentType: "application/json",
            data: JSON.stringify(formData),
            type: "POST",
            dataType: "json",
            success: function(response) {
                $('#addPetModal').hide();
                $('#successAlert').html('Your pet has successfully added!').show();
            }
        });
    });

    $("#openAppointmentModal").on("click", (event) => {
         const vaccineId = $(event.currentTarget).data('vaccine-id');
         $("#editAppointmentForm").attr('data-vaccine-id', vaccineId);
    });

    $("#editAppointmentForm").submit((event) => {
        event.preventDefault();
        $loader.show();
        const vaccineId = $(event.currentTarget).data('vaccine-id');
        const appointmentDate = $(this).find("input[name='appointmentDate']").val();
        $.ajax({
            url: `/api/pets/edit_vaccine_appointment`,
            contentType: "application/json",
            type: "POST",
            data : JSON.stringify({appointment_date: appointmentDate, vaccine_id: vaccineId}),
            dataType: "json",
            success: function(response) {
                window.location.reload();
            }
        });
    });
});