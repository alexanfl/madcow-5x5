$(window).load( () => {
  $( () => {
    $('#squat_primary').bootstrapTable({ 
      data: data.squat_primary,
      columns: columns,
      formatLoadingMessage: () => {
          return ''
      },
      formatShowingRows: () => {
          return ''
      },
    }); 
    $('#bench_primary').bootstrapTable({ 
      data: data.bench_primary,
      columns: columns,
      formatLoadingMessage: () => {
          return ''
      },
      formatShowingRows: () => {
          return ''
      },
    }); 
    $('#row_primary').bootstrapTable({ 
      data: data.row_primary,
      columns: columns,
      formatLoadingMessage: () => {
          return ''
      },
      formatShowingRows: () => {
          return ''
      },
    }); 
    $('#squat_tertiary').bootstrapTable({ 
      data: data.squat_tertiary,
      columns: columns,
      formatLoadingMessage: () => {
          return ''
      },
      formatShowingRows: () => {
          return ''
      },
    }); 
    $('#dl_primary').bootstrapTable({ 
      data: data.dl_primary,
      columns: columns,
      formatLoadingMessage: () => {
          return ''
      },
      formatShowingRows: () => {
          return ''
      },
    }); 
    $('#ohp_primary').bootstrapTable({ 
      data: data.ohp_primary,
      columns: columns,
      formatLoadingMessage: () => {
          return ''
      },
      formatShowingRows: () => {
          return ''
      },
    }); 
    $('#squat_secondary').bootstrapTable({ 
      data: data.squat_secondary,
      columns: columns,
      formatLoadingMessage: () => {
          return ''
      },
      formatShowingRows: () => {
          return ''
      },
    }); 
    $('#bench_secondary').bootstrapTable({ 
      data: data.bench_secondary,
      columns: columns,
      formatLoadingMessage: () => {
          return ''
      },
      formatShowingRows: () => {
          return ''
      },
    }); 
    $('#row_secondary').bootstrapTable({ 
      data: data.row_secondary,
      columns: columns,
      formatLoadingMessage: () => {
          return ''
      },
      formatShowingRows: () => {
          return ''
      },
    }); 
    $('#squat_tertiary').bootstrapTable({ 
      data: data.squat_tertiary,
      columns: columns,
      formatLoadingMessage: () => {
          return ''
      },
      formatShowingRows: () => {
          return ''
      },
    }); 
  });
});

function dataFormatter(value, row, index, field) {
    if (value) {
      html = [value]; 
    }
    else {
        html = ['-']
    }
    return html.join('');
}
