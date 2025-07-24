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
            <Link href="/select-device" className="back">
                Back
            </Link>
            <Form action="">
                <input name="id" value={id} disabled />
                <input name="name" placeholder="Name" />
                <input
                    name="channel-count"
                    type="number"
                    placeholder="Channel Count"
                />
                <button type="submit">Edit</button>
            </Form>
        </>
    )
}
