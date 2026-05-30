export default function ResultsTable({ results }) {

  if (!results.length) {
    return <p>No records found.</p>;
  }

  return (
    <table
      border="1"
      cellPadding="8"
      style={{
        marginTop:"20px",
        width:"100%"
      }}
    >
      <thead>
        <tr>
          <th>Website</th>
          <th>Company</th>
          <th>Email</th>
          <th>Phone</th>
          <th>Core Service</th>
        </tr>
      </thead>

      <tbody>

        {results.map((row,index)=>(
          <tr key={index}>
            <td>{row.website_name}</td>

            <td>{row.company_name}</td>

            <td>
              {row.mail?.join(", ")}
            </td>

            <td>
              {row.mobile_number}
            </td>

            <td>
              {row.core_service}
            </td>

          </tr>
        ))}

      </tbody>
    </table>
  );
}