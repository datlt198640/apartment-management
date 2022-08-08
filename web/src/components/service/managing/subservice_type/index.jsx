import * as React from "react";
import Wrapper from "utils/components/wrapper";
import PageHeading from "utils/components/PageHeading";
import Table from "./Table";
import { messages } from "./config";

export default function Service() {
    return (
        <Wrapper>
            <>
                <PageHeading>
                    <>{messages.heading}</>
                </PageHeading>
                <Table />
            </>
        </Wrapper>
    );
}

Service.displayName = "Service";
