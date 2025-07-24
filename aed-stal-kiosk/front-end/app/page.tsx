import Image from "next/image"

import aedGroup from "@/public/aed-group.png"

export default function Home() {
    return (
        <section className="screen">
            <button className="start">Start</button>
            <Image src={aedGroup} alt="AED Group" className="logo" />
        </section>
    )
}
