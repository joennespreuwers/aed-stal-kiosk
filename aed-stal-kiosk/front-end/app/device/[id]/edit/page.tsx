import Link from "next/link"
import Form from "next/form"

export default async function Select({
    params
}: {
    params: Promise<{ id: string }>
}) {
    const { id } = await params

    return (
        <>
            <Link href={`/device/${id}`} className="back">
                Back
            </Link>
            <Form action="">
                <label>ID</label>
                <input name="id" value={id} disabled />
                <label>Name</label>
                <input name="name" />
                <label>Channel Count</label>
                <input name="channel-count" type="number" />
                <button type="submit">Edit</button>
            </Form>
        </>
    )
}
