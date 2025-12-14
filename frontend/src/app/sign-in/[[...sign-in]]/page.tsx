 "use client";

import { SignIn, useUser } from "@clerk/nextjs";
import { useSearchParams, useRouter } from "next/navigation";

export default function Page() {
  const search = useSearchParams();
  const router = useRouter();
  const { isSignedIn } = useUser();
  const redirect = search?.get("redirect_url") || "/";

  if (isSignedIn) {
    router.push(redirect);
    return null;
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-pink-50">
      <SignIn
        path="/sign-in"
        routing="path"
        signUpUrl={`/sign-up?redirect_url=${encodeURIComponent(redirect)}`}
        fallbackRedirectUrl={redirect}
        forceRedirectUrl={redirect}
      />
    </div>
  );
}
