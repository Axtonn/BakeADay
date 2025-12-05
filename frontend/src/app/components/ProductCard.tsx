import Image from "next/image";

export default function ProductCard({
  name,
  price,
  imgUrl,
  description,
}: {
  name: string;
  price: string;
  imgUrl: string;
  description: string;
}) {
  return (
    <div className="bg-white rounded-2xl shadow-lg flex flex-col items-center p-5">
      <Image
        src={imgUrl}
        alt={name}
        width={24}
        height={300}
        className="w-full h-48 object-cover rounded-t-lg"
        unoptimized
      />
      <h3 className="text-xl font-semibold text-pink-700 mb-1">{name}</h3>
      <p className="text-sm text-pink-800 mb-2">{description}</p>
      <span className="bg-pink-200 text-pink-700 px-3 py-1 rounded-full font-bold">{price}</span>
    </div>
  );
}
