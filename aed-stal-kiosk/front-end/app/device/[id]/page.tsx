import Link from "next/link"

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
            <ul>
                <li>
                    <Link href="#">Frequency Sweep</Link>
                </li>
                <li>
                    <Link href={`/device/${id}/edit`}>Edit</Link>
                </li>
            </ul>
        </>
    )
}
